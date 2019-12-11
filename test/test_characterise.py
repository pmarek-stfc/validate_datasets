import unittest
from characterise import Characterise

class TestCharacterise(unittest.TestCase):

    def setUp(self):
        self.obj_path_correct = Characterise(
            '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/seaIce/day/r1i1p1/v20110113')
        self.obj_path_empty = Characterise('')
        self.obj_path_wrong = Characterise(
            '/rubbis/cmip5/data/nodata')
        self.obj_path_with_dir = Characterise(
            '/home/pmarek/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/seaIce/day/r1i1p1/v20110113/sic')

    def test_check_path_success(self):
        result = self.obj_path_correct.check_path()
        self.assertEqual(result, 'GOOD')

    def test_check_path_fail(self):
        result = self.obj_path_wrong.check_path()
        result2 = self.obj_path_empty.check_path()
        self.assertEqual(result, 'WRONG PATH')
        self.assertEqual(result2, 'WRONG PATH')

    def test_check_varnames_success(self):
        result = self.obj_path_with_dir.check_varnames()
        self.assertEqual(result, 'GOOD')

    def test_check_varnames_fail(self):
        result = self.obj_path_wrong.check_varnames()
        result2 = self.obj_path_empty.check_varnames()
        self.assertEqual(result, set())
        self.assertEqual(result2, set())

    def test_check_var_in_file_success(self):
        result = self.obj_path_with_dir.check_var_in_file()
        self.assertEqual(result, 'GOOD')

    def test_check_var_in_file_fail(self):
        result = self.obj_path_wrong.check_var_in_file()
        result2 = self.obj_path_empty.check_var_in_file()
        self.assertIsNone(result)
        self.assertIsNone(result2)

    def test_check_var_has_coords_success(self):
        result = self.obj_path_with_dir.check_var_has_coords(["time", "lat", "lon"])
        self.assertEqual(result, 'GOOD')

    def test_check_var_has_coords_fail(self):
        result = self.obj_path_wrong.check_var_has_coords(["time", "lat", "lon"])
        result2 = self.obj_path_empty.check_var_has_coords(["time", "lat", "lon"])
        result3 = self.obj_path_with_dir.check_var_has_coords(["time", "nodata", "rubbish"])
        self.assertIsNone(result)
        self.assertIsNone(result2)
        self.assertEqual(result3[0], 'WRONG DIMENSIONS')

    def test_check_lat_in_range_success(self):
        result = self.obj_path_with_dir.check_lat_in_range(-90, 90)
        self.assertEqual(result, 'GOOD')

    def test_check_lat_in_range_fail(self):
        result = self.obj_path_with_dir.check_lat_in_range(-90.5,90.5)
        result2 = self.obj_path_with_dir.check_lat_in_range('rubbish', 90)
        self.assertEqual(result[0], 'INCORRECT RANGE')
        self.assertIsNone(result2)

    def test_check_lon_in_range_success(self):
        result = self.obj_path_with_dir.check_lon_in_range(0, 360)
        self.assertEqual(result, 'GOOD')

    def test_check_lon_in_range_fail(self):
        result = self.obj_path_with_dir.check_lon_in_range(-180, 180)
        result2 = self.obj_path_with_dir.check_lon_in_range('rubbish', 180)
        self.assertEqual(result[0], 'INCORRECT RANGE')
        self.assertIsNone(result2)
