import re
import glob
import os
from dataset_utils import *
import xarray as xr

def open_mfdatasets(files_to_open):
    """
        :param files_to_open: netCDF4 files
        :return: opened netCDF datasets using `open_mfdataset`
    """
    try:
        # ALWAYS USE combine='by_coords' with open_mfdataset
        with xr.open_mfdataset(files_to_open, combine='by_coords') as ds:
            return ds
    except Exception as e:
        return e

def _get_var_id(files_found):
    """
    :param files_found: list of paths to NetCDF4 files
    :return: variable ID of the file
    """
    first_file = files_found[0]
    split_name = first_file.strip('/').split('/')
    file_name = split_name[-1]
    var_id = file_name.strip('_').split('_')[0]
    return var_id

class Characterise:
    def __init__(self, path, project='cmip5', checks={}): #s
        self.path = path
        self.project = project
        self.checks = checks # store results of all checks

    def check_path(self):
        """
            Check if the given path meets certain requirements.
        :return: 'checks' dictionary with a result
        """
        split_path = self.path.strip('/').split('/')
        regex_condition = "v20\d{6}"

        if len(split_path) == 13 and \
                split_path[:2] == ['badc', self.project] and \
                re.search(regex_condition, split_path[-1]):
            self.checks['path_check'] = 'GOOD'
            return self.checks
        else:
            self.checks['path_check'] = 'WRONG PATH'
            return self.checks

    def check_varnames(self):
        """
            Check if NetCDF4 files in a directory start with
            the same variable ID.
        :return: 'checks' dictionary with a result
        """
        var_names = set() # use set to get rid of duplicates
        files_found = glob.glob(self.path + '/*.nc')
        for file in files_found:
            split_name = file.strip('/').split('/')
            file_names = split_name[-1]
            split_file_names = file_names.strip('_').split('_')
            var_names.update([split_file_names[0]])
        if len(var_names) == 1:
            self.checks['varnames_check'] = 'GOOD'
            return self.checks

        self.checks['INCONSISTENT VARIABLE NAMES'] = var_names
        return self.checks

    def check_var_in_file(self):
        """
            Check if a variable ID of a first NetCDF4 file found
            in a directory is present inside the file
        :return: 'checks' dictionary with a result
        """
        files_found = glob.glob(self.path + '/*.nc')
        first_file = files_found[0]
        var_ID = _get_var_id(files_found)

        ds = open_file(first_file)
        if has_variables(ds, [var_ID]):
            self.checks['var_check'] = 'GOOD'
            return self.checks

        self.checks['var_check'] = 'NOT PRESENT'
        return self.checks

    def check_var_has_coords(self, coords):
        """
            Check if the variable ID has coordinates
        :param coords: list of coords for example ["time", "lat", "lon"]
        :return: 'checks' dictionary with a result
        """
        files_found = glob.glob(self.path + '/*.nc')
        var_id = _get_var_id(files_found)

        ds = open_mfdatasets(files_found)
        a = set(list(ds[var_id].indexes.keys()))
        if a.issubset(coords):
            self.checks['coords_check'] = 'GOOD'
            return self.checks
        self.checks['coords_check'] = 'WRONG DIMENSIONS', a
        return self.checks

    def check_lat_in_range(self, lower_bnd, upper_bnd):
        """
            Check range of latitude
        :param lower_bnd: lower bound latitude
        :param upper_bnd: upper bound latitude
        :return: 'checks' dictionary with a result
        """
        files_found = glob.glob(self.path + '/*.nc')
        ds = open_mfdatasets(files_found)
        result = is_in_range(ds, 'lat', lower_bnd, upper_bnd)
        if result:
            self.checks['latitude_check'] = 'GOOD'
            return self.checks
        self.checks['latitude_check'] = 'INCORRECT RANGE', (lower_bnd, upper_bnd)
        return self.checks

    def check_lon_in_range(self, lower_bnd, upper_bnd):
        """
            Check range of longitude
        :param lower_bnd: lower bound longitude
        :param upper_bnd: upper bound longitude
        :return: 'checks' dictionary with a result
        """
        files_found = glob.glob(self.path + '/*.nc')
        ds = open_mfdatasets(files_found)
        result = is_in_range(ds, 'lon', lower_bnd, upper_bnd)
        if result:
            self.checks['longitude_check'] = 'GOOD'
            return self.checks
        self.checks['longitude_check'] = 'INCORRECT RANGE', (lower_bnd, upper_bnd)
        return self.checks


if __name__=='__main__':
    test_check_path = Characterise('/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/seaIce/day/r1i1p1/v20110113')
    print(test_check_path.check_path())
    test_check_varnames = Characterise('/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/seaIce/day/r1i1p1/v20110113/sic')
    print(test_check_varnames.check_varnames())
    test_check_var_in_file = Characterise('/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/seaIce/day/r1i1p1/v20110113/sic')
    print(test_check_var_in_file.check_var_in_file())
    test_check_var_has_coords = Characterise(
        '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/seaIce/day/r1i1p1/v20110113/sic')
    print(test_check_var_has_coords.check_var_has_coords(["time", "lat", "lon"]))
    test_check_lat_in_range = Characterise(
        '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/seaIce/day/r1i1p1/v20110113/sic')
    print(test_check_lat_in_range.check_lat_in_range(-90, 90))
    test_check_lon_in_range = Characterise(
        '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/seaIce/day/r1i1p1/v20110113/sic')
    print(test_check_lon_in_range.check_lon_in_range(0, 90))