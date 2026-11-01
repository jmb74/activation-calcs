"""Regression tests for region identity, decay times and state preservation."""
import tempfile
import unittest
from pathlib import Path

from process_rn_tab import read_table, validate_geometry

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'working/cycloinv_target2_cleanv6'


class ReaderTests(unittest.TestCase):
    def test_v6_geometry_and_nonsequential_cooling_names(self):
        table = Path(f'{BASE}_22_tab.lis')
        ds = read_table(table, Path(f'{BASE}_22_sum.lis'))
        regions = validate_geometry(ds, Path(f'{BASE}_01.inp'), table)
        self.assertEqual(regions[8], 'TGT')
        self.assertEqual(regions[5], 'TAWIN')
        self.assertEqual(len(ds), 204)
        self.assertEqual(len({d.cooling_time_s for d in ds}), 34)
        by_name = {d.name: d for d in ds}
        self.assertEqual(by_name['D003R4'].cooling_time_s, 86400)
        self.assertEqual(by_name['D004R4'].cooling_time_s, 604800)
        self.assertEqual(by_name['D001R4'].region_number, 8)

    def fixture(self, directory):
        table = directory / 'sample_22_tab.lis'
        summary = directory / 'sample_22_sum.lis'
        table.write_text('# Detector n: 1\nA\n# A/Z Isotopes:\n'
                         '24 11 2.000 10.0\n# A/Z/m Isomers:\n24 11 1 3.000 20.0\n')
        summary.write_text('Total primaries run: 10\nBeam intensity: 1E12 pr/s\n'
                           'Irradiation time: 604800 s\nDecay time: 7200 s\n'
                           'Detector n: 1 A\n(Region 8 Volume: 2.0 cmc,\n'
                           'Tot. response (Bq/cmc) 5.000 +/- 1.0 %\n')
        return table, summary

    def test_last_isomer_and_normalization(self):
        with tempfile.TemporaryDirectory() as tmp:
            table, summary = self.fixture(Path(tmp))
            d, = read_table(table, summary)
            self.assertEqual([(n.label, n.value) for n in d.nuclides],
                             [('Na-24', 4.), ('Na-24-m1', 6.)])
            self.assertAlmostEqual(d.nuclides[-1].absolute_error, 1.2)
            self.assertEqual(d.total, 10.)

    def test_truncated_last_state_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            table, summary = self.fixture(Path(tmp))
            table.write_text(table.read_text().rsplit('24 11 1', 1)[0])
            with self.assertRaisesRegex(ValueError, 'sum disagrees'):
                read_table(table, summary)

    def test_renumbered_geometry_refused(self):
        table = Path(f'{BASE}_22_tab.lis')
        ds = read_table(table, Path(f'{BASE}_22_sum.lis'))
        with tempfile.TemporaryDirectory() as tmp:
            geometry = Path(tmp) / 'wrong.inp'
            source = Path(f'{BASE}_01.inp').read_text()
            source = source.replace('WAT          5', 'WRONG        5')
            geometry.write_text(source)
            with self.assertRaisesRegex(ValueError, 'region mismatch'):
                validate_geometry(ds, geometry, table)


if __name__ == '__main__':
    unittest.main()
