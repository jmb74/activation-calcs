#!/usr/bin/env python3
"""Compare the supplied MCNP 6.3.0 output with processed FLUKA results. No runs."""
import csv,hashlib,json,math,re,sys
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'working';R=ROOT/'reference';O=ROOT/'results/mcnp-comparison-20261026'
sys.path.insert(0,str(ROOT.parent/'fluka-util'))
from process_rn_tab import read_table,SYMBOLS
MC=R/'racl2_30MeV_good_flowandflux_fine.io'

def writecsv(path,rows):
    with path.open('x',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def parse_mcnp(path):
    text=path.read_text();out={}
    for block in re.split(r'^1tally\s+',text,flags=re.M)[1:]:
        m=re.match(r'(\d+)\s+nps\s*=\s*(\d+)',block)
        if not m:continue
        histories=int(m[2]);tally=int(m[1]);rows=defaultdict(dict);totals={};columns=None
        for line in block.splitlines()[1:]:
            if 'results of 10 statistical checks' in line:break
            m=re.match(r'\s*(segment|cell):\s+(.+)',line)
            if m:
                columns=[int(x) if x!='whole' else 19 for x in m[2].split()];continue
            if columns:
                parts=line.split()
                if len(parts)!=1+2*len(columns):continue
                try:values=[float(x) for x in parts[1:]]
                except ValueError:continue
                if parts[0]=='total':
                    totals.update({c:dict(value=values[2*i],relative_error=values[2*i+1]) for i,c in enumerate(columns)})
                else:
                    try:key=float(parts[0])
                    except ValueError:continue
                    for i,c in enumerate(columns):
                        assert c not in rows[key],(tally,key,c)
                        rows[key][c]=dict(value=values[2*i],relative_error=values[2*i+1])
        out[tally]=dict(histories=histories,rows=dict(rows),totals=totals)
    assert set(out)=={1,2,11,12,18,21,22,32,42},out.keys()
    for t in [1,2,11,12,21,22]:
        assert set(out[t]['totals'])==set(range(1,20))
        for col,total in out[t]['totals'].items():
            assert math.isclose(sum(r[col]['value'] for r in out[t]['rows'].values()),total['value'],rel_tol=2e-5), (t,col)
    for t in [1,11,21]:assert math.isclose(sum(out[t]['totals'][i]['value'] for i in range(1,19)),out[t]['totals'][19]['value'],rel_tol=2e-5)
    assert set(out[18]['totals'])=={1,2,3,4,5}
    for c,total in out[18]['totals'].items():assert math.isclose(sum(r[c]['value'] for r in out[18]['rows'].values()),total['value'],rel_tol=2e-5),(18,c)
    return out

def read_bdx(unit):
    text=(W/f'cycloinv_6061_1m_{unit}_sum.lis').read_text();totals={}
    for block in re.split(r'\n\s*Detector n:',text)[1:]:
        m=re.match(r'\s*\d+\s*\(\s*\d+\s*\)\s+(\w+)',block);assert m
        match=re.search(r'Tot\. resp\.\s*\([^)]+\)\s*(\S+)\s*\+/-\s*(\S+)',block);assert match
        area=re.search(r'Area:\s*(\S+)',block)
        totals[m[1]]=dict(value=float(match[1]),error_percent=float(match[2]),area=float(area[1]))
    spectra={};active=False
    for line in (W/f'cycloinv_6061_1m_{unit}_tab.lis').read_text().splitlines():
        m=re.match(r'\s*# Detector n:\s*\d+\s+(\w+)\s+\(integrated',line)
        if m:name=m[1];spectra[name]=[];active=True;continue
        if 'double differential distributions' in line:active=False
        if active and line.strip() and not line.lstrip().startswith('#'):
            v=list(map(float,line.split()));assert len(v)==4;spectra[name].append(v)
    return totals,spectra

def rebin(rows,low_MeV,high_MeV):
    lo=low_MeV/1000;hi=high_MeV/1000
    return sum(max(0,min(b,hi)-max(a,lo))*v for a,b,v,e in rows)

def main():
    assert not O.exists() or not any(O.iterdir()),O;O.mkdir(parents=True,exist_ok=True)
    mc=parse_mcnp(MC);ft,fs=read_bdx(32)
    scalar=[];angular=[];spectral=[]
    for sp,particle,current_t,flux_t in [('N','neutron',1,2),('G','photon',21,22),('P','proton',11,12)]:
        for quantity,t in [('J',current_t),('F',flux_t)]:
            if quantity=='J':fv=sum(ft[f'M0{sp}J{i:02}']['value'] for i in range(1,19))
            else:fv=sum(ft[f'M0{sp}F{i:02}']['value']*ft[f'M0{sp}F{i:02}']['area'] for i in range(1,19))/(4*math.pi*10000)
            mv=mc[t]['totals'][19]['value']
            scalar.append(dict(particle=particle,score='current' if quantity=='J' else 'fluence',unit='crossings/primary' if quantity=='J' else 'cm^-2/primary',mcnp=mv,mcnp_relative_error_percent=mc[t]['totals'][19]['relative_error']*100,fluka=fv,fluka_over_mcnp=fv/mv))
            for i in range(1,19):
                fl=ft[f'M0{sp}{quantity}{i:02}'];m=mc[t]['totals'][19-i]
                angular.append(dict(particle=particle,score=quantity,fluka_band=i,mcnp_segment=19-i,mcnp=m['value'],mcnp_error_percent=m['relative_error']*100,fluka=fl['value'],fluka_error_percent=fl['error_percent'],fluka_over_mcnp=fl['value']/m['value'] if m['value'] else None))
        # Compare whole-sphere current spectra in MCNP's arbitrary bins.
        low=0
        for high,values in sorted(mc[current_t]['rows'].items()):
            fl=sum(rebin(fs[f'M0{sp}J{i:02}'],low,high) for i in range(1,19))
            mv=values[19]['value']
            spectral.append(dict(particle=particle,energy_low_MeV=low,energy_high_MeV=high,mcnp_crossings_per_primary=mv,mcnp_relative_error_percent=values[19]['relative_error']*100,fluka_crossings_per_primary=fl,fluka_over_mcnp=fl/mv if mv else None))
            low=high
    prod=read_table(W/'cycloinv_6061_1m_21_tab.lis',W/'cycloinv_6061_1m_21_sum.lis')
    # Compare isotope sums because MCNP combines isomeric residual states.
    mapping={4:('TGT','Y4'),5:('ALCASE','Y0'),2:('WAT','Y2'),1:('HAV1','Y1'),3:('HAV2','Y3')};nuclides=[]
    for cell,(region,name) in mapping.items():
        det=next(d for d in prod if d.name==name);byid=defaultdict(list)
        for n in det.nuclides:
            if n.value:byid[(n.z,n.a)].append(n)
        mr={}
        for key,values in mc[18]['rows'].items():
            za=round(key);assert abs(key-za)<1e-6
            z,a=divmod(za,1000);assert 1<=z<len(SYMBOLS)
            if values[cell]['value']:mr[z,a]=values[cell]
        for z,a in sorted(set(byid)|set(mr)):
            ns=byid.get((z,a),[]);fv=sum(n.value for n in ns);mv=mr.get((z,a),{}).get('value',0)
            nuclides.append(dict(region=region,mcnp_cell=cell,isotope=f'{SYMBOLS[z]}-{a}',z=z,a=a,mcnp_nuclei_per_primary=mv,mcnp_relative_error_percent=mr.get((z,a),{}).get('relative_error',0)*100,fluka_nuclei_per_primary=fv,fluka_states=';'.join(n.label for n in ns),fluka_relative_error_percent=ns[0].relative_error_percent if len(ns)==1 else None,fluka_over_mcnp=fv/mv if mv else None))
    writecsv(O/'integrated-spectra-comparison.csv',scalar);writecsv(O/'angular-comparison.csv',angular);writecsv(O/'spectra-mcnp-bins.csv',spectral);writecsv(O/'residual-production-comparison.csv',nuclides)
    summary=dict(mcnp_source=str(MC.relative_to(ROOT)),mcnp_version='6.3.0',mcnp_histories=500000000,fluka_histories=40000000,integrated=scalar,target=[r for r in nuclides if r['region']=='TGT' and r['isotope'] in ['Ac-223','Ac-224','Ac-225','Ac-226','Ra-224','Ra-225','Ra-226','Cl-34','Cl-36']],sources_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [MC,W/'cycloinv_6061_1m_21_tab.lis',W/'cycloinv_6061_1m_32_sum.lis']})
    (O/'comparison-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(2,3,figsize=(14,8),layout='constrained')
    for col,(sp,title) in enumerate([('neutron','Neutrons'),('photon','Photons'),('proton','Protons')]):
        rr=[r for r in spectral if r['particle']==sp and r['energy_low_MeV']>0]
        edges=[rr[0]['energy_low_MeV']]+[r['energy_high_MeV'] for r in rr]
        for key,label in [('mcnp_crossings_per_primary','MCNP'),('fluka_crossings_per_primary','FLUKA')]:
            axes[0,col].stairs([r[key]/(r['energy_high_MeV']-r['energy_low_MeV']) for r in rr],edges,label=label)
        axes[0,col].set(xscale='log',yscale='log',title=title,xlabel='Energy (MeV)',ylabel='Crossings / primary / MeV');axes[0,col].legend();axes[0,col].grid(alpha=.2)
        rows=[r for r in angular if r['particle']==sp and r['score']=='J']
        for key,label in [('mcnp','MCNP'),('fluka','FLUKA')]:
            total=sum(r[key] for r in rows);axes[1,col].plot(range(1,19),[r[key]/total for r in rows],marker='.',label=label)
        axes[1,col].set(xlabel='Spatial band (1 forward, 18 backward)',ylabel='Fraction of total crossings');axes[1,col].grid(alpha=.2)
    fig.savefig(O/'mcnp-fluka-spectra.png',dpi=170)
if __name__=='__main__':main()
