"""Photon export regression checks for normalization and geometry."""
import csv
import math
import tempfile
import unittest
from pathlib import Path

from export_photons import export_photons, export_prompt_neutrons, read_input, read_spectra


def card(tag, *fields, name=''):
    return f'{tag:<10}' + ''.join(f'{str(f):>10}' for f in (*fields, *(['']*(6-len(fields))))) + name + '\n'


class PhotonTests(unittest.TestCase):
    def fixture(self, root):
        geometry = root/'run.inp'
        geometry.write_text('''GEOBEGIN                                                              COMBNAME
    0 0 example
SPH world 0 0 0 100
RCC outer 0 0 0 0 0 1.655 1.2
RCC inner 0 0 0.05 0 0 1.405 1
END
BLKHOLE 5 -world
VACREG 5 +world -outer
ALCASE 5 +outer -inner
END
GEOEND
''' + card('IRRPROFI',604800,10) + card('DCYTIMES',0,3600)
            + card('USRBDX',1,'PHOTON',-38,'ALCASE','VACREG',2,name='G002LTOT')
            + card('USRBDX',.000003,.000001,2,6.28318531,0,1,name='&')
            + card('DCYSCORE',2,'','','G002LTOT','G002LTOT',1,name='USRBDX')
            + card('USRBDX',1,'PHOTON',-24,'ALCASE','VACREG',2,name='PRGTOT')
            + card('USRBDX',.000003,.000001,2,6.28318531,0,1,name='&'))
        tables = []
        for unit, name in ((38, 'G002LTOT'), (24, 'PRGTOT')):
            table = root/f'run_{unit}_tab.lis'
            table.write_text(f' # Detector n: 1 {name} (integrated over solid angle)\n'
                             ' # N. of energy intervals 2\n'
                             '1e-6 2e-6 1e6 10\n2e-6 3e-6 2e6 20\n'
                             ' # double differential distributions\n'
                             '1e-6 2e-6 9e99 10\n')
            table.with_name(f'run_{unit}_sum.lis').write_text(
                f' Detector n: 1 (1) {name}\n (Area: 2.0 cmq,\n'
                'from reg. 3 to 2,\none way scoring,\ncurrent scoring)\n'
                'Tot. resp. (Part/cmq/pr) 3.0 +/- 5.0 %\n')
            tables.append(table)
        return geometry, tables

    def test_units_area_prompt_scaling_and_angular_exclusion(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            geometry, tables = self.fixture(root)
            self.assertEqual(len(read_spectra(tables[0])['G002LTOT']), 2)
            export_photons(tables, geometry, root/'out')
            def rows(kind):
                with (root/f'out/photon-escaping-{kind}.csv').open() as f:
                    return list(csv.DictReader(f))
            delayed, prompt = rows('delayed')[0], rows('prompt')[0]
            self.assertEqual(float(delayed['cooling_time_s']), 3600)
            self.assertAlmostEqual(float(delayed['escaping_photons_per_s_per_MeV']), 2000)
            self.assertAlmostEqual(float(delayed['escaping_photons_per_s_in_bin']), 2)
            self.assertAlmostEqual(float(delayed['absolute_statistical_error_photons_per_s_in_bin']), .2)
            area = 2*math.pi*1.2*(1.2+1.655)
            self.assertAlmostEqual(float(delayed['surface_average_outward_current_photons_per_cm2_s_in_bin']), 2/area)
            self.assertAlmostEqual(float(prompt['escaping_photons_per_s_in_bin']), 20)
            self.assertAlmostEqual(float(prompt['escaping_photons_per_primary_in_bin']), 2)

    def test_scalar_fluence_input_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            geometry, _ = self.fixture(Path(tmp))
            geometry.write_text(geometry.read_text().replace('USRBDX             1', 'USRBDX           101'))
            with self.assertRaisesRegex(ValueError, 'current scoring'):
                read_input(geometry)

    def test_missing_bin_refused_before_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            geometry, tables = self.fixture(root)
            tables[0].write_text(tables[0].read_text().replace('2e-6 3e-6 2e6 20\n', ''))
            with self.assertRaisesRegex(ValueError, 'bin count'):
                export_photons(tables, geometry, root/'out')
            self.assertFalse((root/'out').exists())

    def test_neutron_species_selection_and_units(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            geometry, tables = self.fixture(root)
            geometry.write_text(geometry.read_text()
                + card('USRBDX',1,'NEUTRON',-24,'ALCASE','VACREG',2,name='PRNTOT')
                + card('USRBDX',.000003,.000001,2,6.28318531,0,1,name='&'))
            table = tables[1]
            table.write_text(table.read_text().replace('PRGTOT', 'PRNTOT'))
            summary = root/'run_24_sum.lis'
            summary.write_text(summary.read_text().replace('PRGTOT', 'PRNTOT'))
            export_prompt_neutrons(table, geometry, root/'out')
            with (root/'out/neutron-escaping-prompt.csv').open() as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]['detector'], 'PRNTOT')
            self.assertAlmostEqual(float(rows[0]['escaping_neutrons_per_s_in_bin']),20)
            self.assertAlmostEqual(float(rows[0]['escaping_neutrons_per_primary_in_bin']),2)
            self.assertFalse(any('photons' in k for k in rows[0]))


if __name__ == '__main__':
    unittest.main()
