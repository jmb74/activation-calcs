#!/usr/bin/env python3
"""Read existing processed 6061 run products; never starts or modifies a run."""
import csv,hashlib,json,math,re
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]; W=ROOT/'working'; O=ROOT/'results/review-6061-1m-20261026'; PREFIX='cycloinv_6061_1m'

def writecsv(path,rows):
    with path.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
def num(x):return float(x.replace('D','E'))
def totals(unit):
    text=(W/f'{PREFIX}_{unit}_sum.lis').read_text(); result={}
    for block in re.split(r'\n\s*Detector n:',text)[1:]:
        header=re.match(r'\s*(\d+)\s*(?:\(\s*\d+\s*\))?\s+(\w+)',block); assert header,block[:80]
        match=re.search(r'Tot\. resp(?:onse|\.)\s*\([^)]+\)\s*(\S+)\s*\+/-\s*(\S+)',block); assert match,block[:300]
        area=re.search(r'Area:\s*(\S+)',block)
        result[header[2]]=dict(value=num(match[1]),relative_error_percent=num(match[2]),area_cm2=num(area[1]) if area else 1)
    return result

def spectra(unit):
    result={};name=None;active=False
    for line in (W/f'{PREFIX}_{unit}_tab.lis').read_text().splitlines():
        m=re.match(r'\s*# Detector n:\s*\d+\s+(\w+)\s+\(integrated over solid angle\)',line)
        if m:name=m[1];result[name]=[];active=True;continue
        if 'double differential distributions' in line:active=False
        if active and line.strip() and not line.lstrip().startswith('#'):
            vals=list(map(num,line.split()));assert len(vals)==4
            result[name].append(vals)
    return result
status=[];diagnostics=Counter();warnings=Counter()
for p in sorted(W.glob(f'{PREFIX}_0*.out')):
    t=p.read_text();m=re.search(r'Total number of primaries run:\s*(\d+)',t)
    cpu=re.search(r'Total CPU time used to follow all primary particles:\s*(\S+)',t)
    assert m and 'End of FLUKA v4 run' in t,p
    assert not re.search('abort|fatal|lost particle|geometry error',t,re.I),p
    status.append(dict(file=p.name,primaries=int(m[1]),cpu_seconds=num(cpu[1]),normal_end=True))
    warnings.update(re.findall(r'\*\*\*\* Warning!!! (.+)',t))
for p in W.glob(f'{PREFIX}_0*.err'):
    for line in p.read_text().splitlines():
        if line.startswith(' ***'):diagnostics[line.split()[1]]+=1
assert len(status)==40 and sum(r['primaries'] for r in status)==40000000
writecsv(O/'cycle-status.csv',status)
a=list(csv.DictReader((O/'activity-all-regions.csv').open()));prod=list(csv.DictReader((O/'production-all-regions.csv').open()))
for name,rows in [('target-activity.csv',[r for r in a if r['detector'].endswith('R4')]),('target-production.csv',[r for r in prod if r['detector']=='Y4'])]:writecsv(O/name,rows)
# Individual table rounded rows should agree with independently printed detector totals.
rt=totals(22)
regions=['ALCASE','HAV1','WAT','HAV2','TGT'];regional=[]
for name,values in rt.items():
    row_sum=sum(float(r['value']) for r in a if r['detector']==name)
    assert math.isclose(row_sum,values['value'],rel_tol=3e-5),(name,row_sum,values)
    regional.append(dict(detector=name,region=regions[int(name[-1])],cooling_s=[0,3600,86400,604800][int(name[1:4])-1],activity_Bq=values['value'],relative_error_percent=values['relative_error_percent']))
writecsv(O/'regional-activity.csv',regional)
all_totals={u:totals(u) for u in [24,25,31,32,34,35,36,37]}
all_spectra={u:spectra(u) for u in [31,32,34,35,36,37]}
# Integrate printed differential columns as a cross-check; tab.lis has rounded boundaries/values.
checks=[]
for u,ss in all_spectra.items():
    for n,rows in ss.items():
        value=sum((hi-lo)*v for lo,hi,v,e in rows);expected=all_totals[u][n]['value']
        difference=abs(value-expected)/abs(expected) if expected else abs(value)
        assert difference<.01,(u,n,value,expected,difference)
        checks.append(difference)
# Proton crossing-energy moments, approximated from 0.2 MeV bins.
proton={}
for name,rows in all_spectra[31].items():
    weights=[(hi-lo)*v for lo,hi,v,e in rows];total=sum(weights)
    def fraction(low,high):
        return sum(max(0,min(hi,high/1000)-max(lo,low/1000))*v for lo,hi,v,e in rows)/total
    def qtile(q):
        cum=0
        for (lo,hi,v,e),weight in zip(rows,weights):
            if cum+weight>=q*total and weight:return 1000*(lo+(hi-lo)*(q*total-cum)/weight)
            cum+=weight
        return rows[-1][1]*1000
    proton[name]=dict(crossings_per_primary=all_totals[31][name]['value'],relative_error_percent=all_totals[31][name]['relative_error_percent'],mean_MeV=sum((hi+lo)*500*wt for (lo,hi,v,e),wt in zip(rows,weights))/total,median_MeV=qtile(.5),q05_MeV=qtile(.05),q95_MeV=qtile(.95),fraction_12_17_MeV=fraction(12,17),fraction_above_20_MeV=fraction(20,40))
# Sphere aggregate values: sums are correlated; do not invent aggregate errors.
area=4*math.pi*10000;rate=249660360000000;sphere=[];bands=[]
for u in [32,34,35,36,37]:
    cool=0 if u==32 else u-33
    for sp in ('N','P','G') if not cool else ('N','G'):
        current=sum(all_totals[u][f'M{cool}{sp}J{i:02}']['value'] for i in range(1,19))
        fluence=sum(all_totals[u][f'M{cool}{sp}F{i:02}']['value']*all_totals[u][f'M{cool}{sp}F{i:02}']['area_cm2'] for i in range(1,19))/area
        sphere.append(dict(unit=u,cooling_s=None if cool==0 else [0,3600,86400,604800][cool-1],particle=sp,kind='prompt' if not cool else 'decay',crossings_per_primary_or_s=current,average_fluence_per_primary_or_s_cm2=fluence,crossings_per_s=current*rate if not cool else current,average_fluence_rate_cm2_s=fluence*rate if not cool else fluence))
        for i in range(1,19):
            f=all_totals[u][f'M{cool}{sp}F{i:02}'];j=all_totals[u][f'M{cool}{sp}J{i:02}']
            bands.append(dict(unit=u,particle=sp,cooling_index=cool,band=i,fluence=f['value'],fluence_error_percent=f['relative_error_percent'],current=j['value'],current_error_percent=j['relative_error_percent']))
writecsv(O/'sphere-integrated.csv',sphere);writecsv(O/'sphere-bands.csv',bands)
# Compare integrated prompt apparatus current to the 1 m sphere, matching energy acceptance caveat.
leakage={}
for sp,label in [('N','N'),('G','P')]:
    exterior=sum(all_totals[24][f'PR{label}{face}J']['value'] for face in ('A','H'))*11.97351007272
    sphere_current=next(r['crossings_per_primary_or_s'] for r in sphere if r['unit']==32 and r['particle']==sp)
    leakage[sp]=dict(apparatus_crossings_per_primary=exterior,sphere_crossings_per_primary=sphere_current,ratio=sphere_current/exterior if exterior else None)
summary=dict(cycles=len(status),primaries=sum(r['primaries'] for r in status),cpu_seconds_sum=sum(r['cpu_seconds'] for r in status),diagnostics=dict(diagnostics),initialization_warnings=dict(warnings),proton=proton,sphere=sphere,leakage=leakage,tab_integral_max_relative_difference=max(checks),activity_rows=len(a),production_rows=len(prod),source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [W/f'{PREFIX}_01.inp',W/f'{PREFIX}_22_tab.lis',W/f'{PREFIX}_22_sum.lis',W/f'{PREFIX}_32_sum.lis']})
(O/'review-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
# Standalone scientific plot, using existing local Matplotlib only.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,axes=plt.subplots(1,3,figsize=(15,4.6),layout='constrained')
ax=axes[0]
for name in ['PIN','POUT']:
    rows=all_spectra[31][name];ax.stairs([v/1000 for lo,hi,v,e in rows],[rows[0][0]*1000]+[r[1]*1000 for r in rows],label=name)
ax.set(xlabel='Proton energy (MeV)',ylabel='Crossings / primary / MeV',title='Salt entrance and case-facing exits',xlim=(0,30));ax.legend();ax.grid(alpha=.2)
ax=axes[1]
for sp,label in [('N','Neutron'),('P','Proton'),('G','Photon')]:
    sets=[all_spectra[32][f'M0{sp}J{i:02}'] for i in range(1,19)];rows=sets[0]
    ax.stairs([sum(ss[k][2] for ss in sets)/1000 for k in range(len(rows))],[rows[0][0]*1000]+[r[1]*1000 for r in rows],label=label)
ax.set(xscale='log',yscale='log',xlabel='Energy (MeV)',ylabel='Crossings / primary / MeV',title='Prompt spectra over the 1 m sphere',xlim=(1e-9,50));ax.legend();ax.grid(alpha=.2)
ax=axes[2]
for isotope in ['Ac-225','Ac-224','Ac-226','Ra-224','Ra-225']:
    rr=[r for r in a if r['detector'].endswith('R4') and r['isotope']==isotope]
    ax.plot([float(r['cooling_time_s'])/86400 for r in rr],[float(r['value'])/1e9 for r in rr],marker='o',label=isotope)
ax.set(yscale='log',xlabel='Cooling time (days)',ylabel='Target activity (GBq)',title='Selected irradiation-produced nuclides',ylim=(.01,100));ax.legend(fontsize=8);ax.grid(alpha=.2)
fig.savefig(O/'run-review.png',dpi=180)
