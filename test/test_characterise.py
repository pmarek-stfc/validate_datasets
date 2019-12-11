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
        self.assertEqual(result['path_check'], 'GOOD')

    def test_check_path_fail(self):
        result = self.obj_path_wrong.check_path()
        self.assertEqual(result['path_check'], 'WRONG PATH')

    def test_check_varnames_success(self):
        result = self.obj_path_with_dir.check_varnames()
        self.assertEqual(result['varnames_check'], 'GOOD')

    def test_check_varnames_fail(self):
        result = self.obj_path_wrong.check_varnames()
        result2 = self.obj_path_empty.check_varnames()
        self.assertIn('INCONSISTENT VARIABLE NAMES', result)
        self.assertIn('INCONSISTENT VARIABLE NAMES', result2)

    def test_check_var_in_file_success(self):
        result = self.obj_path_with_dir.check_var_in_file()
        self.assertEqual(result['var_check'], 'GOOD')

    def test_check_var_in_file_fail(self):
        result = self.obj_path_wrong.check_var_in_file()
        result2 = self.obj_path_empty.check_var_in_file()
        self.assertIsNone(result)
        self.assertIsNone(result2)

    def test_check_var_has_coords_success(self):
        result = self.obj_path_with_dir.check_var_has_coords(["time", "lat", "lon"])
        self.assertEqual(result['coords_check'], 'GOOD')

    def test_check_var_has_coords_fail(self):
        result = self.obj_path_wrong.check_var_has_coords(["time", "lat", "lon"])
        result2 = self.obj_path_empty.check_var_has_coords(["time", "lat", "lon"])
        self.assertIsNone(result)
        self.assertIsNone(result2)

    def test_check_lat_in_range_success(self):
        result = self.obj_path_with_dir.check_lat_in_range(-90, 90)
        self.assertEqual(result['latitude_check'], 'GOOD')
    #
    # def test_check_lat_in_range_fail(self):
    #     pass
    #
    # def test_check_lon_in_range_success(self):
    #     pass
    #
    # def test_check_lon_in_range_fail(self):
    #     pass
    #
    # def test_return_tuple_result_success(self):
    #     pass
    #
    # def test_return_tuple_result_fail(self):
    #     pass
