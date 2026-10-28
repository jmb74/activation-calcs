import contextlib
import csv
import importlib.util
import io
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('cooling', ROOT/'scripts/export-cooling-products.py')
cooling = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cooling)
from process_rn_tab import Detector, Nuclide


class CoolingExports(unittest.TestCase):
    def fixtures(self, folder):
        table=folder/'table.lis';table.write_text('source fixture\n')
        summary=folder/'summary.lis'
        summary.write_text('Beam intensity  : 2.49660342E+14 pr/s\nIrradiation time: 604800.000 s\n')
        detectors=[]
        for t in cooling.TIMES:
            for region in cooling.REGIONS:
                d=Detector(len(detectors)+1,f'D{len(detectors)}',region_number=region,cooling_time_s=t,normalization=1.,value_unit='Bq')
                d.nuclides=[Nuclide(34,17,0,float(region+t+1),5.),Nuclide(34,17,1,float(region+2*t+1),7.)]
                detectors.append(d)
        return table,summary,detectors

    def test_wide_export_scaling_and_isomers(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory);table,summary,detectors=self.fixtures(folder)
            with patch.object(cooling,'read_table',return_value=detectors),contextlib.redirect_stdout(io.StringIO()):
                cooling.export(table,summary,folder/'export',40,400)
            with (folder/'export/TGT.csv').open() as stream:
                rows=list(csv.DictReader(stream))
            self.assertEqual([r['isotope'] for r in rows],['Cl-34','Cl-34-m1'])
            for time in cooling.TIMES:
                self.assertEqual(float(rows[0][f'activity_{time}s']),10*(7+time+1))
                self.assertEqual(float(rows[1][f'activity_{time}s']),10*(7+2*time+1))
                self.assertEqual(float(rows[0][f'relative_error_{time}s_percent']),5)
            with (folder/'export/all-components-summed.csv').open() as stream:
                summed=list(csv.DictReader(stream))
            self.assertFalse(any('upper_bound' in c for c in summed[0]))
            self.assertEqual(float(summed[0]['activity_0s']),sum(10*(r+1) for r in cooling.REGIONS))

    def test_reject_mislabeled_source_current(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory);table,summary,_=self.fixtures(folder)
            with self.assertRaisesRegex(ValueError,'disagrees'):
                cooling.export(table,summary,folder/'export',400)
            self.assertFalse((folder/'export').exists())

    def test_reject_duplicate_missing_time(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory);table,summary,detectors=self.fixtures(folder)
            detectors[-1]=detectors[-2]
            with patch.object(cooling,'read_table',return_value=detectors),self.assertRaisesRegex(ValueError,'Duplicate'):
                cooling.export(table,summary,folder/'export',40)
            self.assertFalse((folder/'export').exists())

    def test_decay_and_ingrowth_remain_linear_in_production(self):
        # Independent two-member Bateman solution: precursor -> long-lived daughter.
        l1=math.log(2)/(11.03*86400);l2=math.log(2)/(2.6234*365.25*86400);T=604800
        def activities(rate,t):
            n1=rate/l1*(1-math.exp(-l1*T))
            n2=rate*((1-math.exp(-l2*T))/l2-(math.exp(-l1*T)-math.exp(-l2*T))/(l2-l1))
            return (l1*n1*math.exp(-l1*t),l2*(n2*math.exp(-l2*t)+l1*n1/(l2-l1)*(math.exp(-l1*t)-math.exp(-l2*t))))
        for time in cooling.TIMES:
            low=activities(1.6e8,time);high=activities(1.6e9,time)
            for a,b in zip(low,high):self.assertTrue(math.isclose(b,10*a,rel_tol=1e-13))
        self.assertGreater(activities(1.6e8,604800)[1],activities(1.6e8,0)[1])


if __name__=='__main__':unittest.main()
