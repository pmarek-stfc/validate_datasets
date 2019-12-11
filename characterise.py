import re
from dataset_utils import *


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
    def __init__(self, path, project='cmip5', checks={}):
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
            print(f'path_check: GOOD')
            return self.checks['path_check']
        else:
            self.checks['path_check'] = 'WRONG PATH'
            print(f'path_check: WRONG PATH')
            return self.checks['path_check']

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
            print(f'varnames_check: GOOD')
            return self.checks['varnames_check']

        self.checks['INCONSISTENT VARIABLE NAMES'] = var_names
        print(f'varnames_check: INCONSISTENT VARIABLE NAMES')
        return self.checks['INCONSISTENT VARIABLE NAMES']

    def check_var_in_file(self):
        """
            Check if a variable ID of a first NetCDF4 file found
            in a directory is present inside the file
        :return: 'checks' dictionary with a result
        """
        files_found = glob.glob(self.path + '/*.nc')
        try:
            first_file = files_found[0]
        except IndexError:
            return None
        var_ID = _get_var_id(files_found)

        ds = open_file(first_file)
        if has_variables(ds, [var_ID]):
            self.checks['var_check'] = 'GOOD'
            print(f'var_check: GOOD')
            return self.checks['var_check']

        self.checks['var_check'] = 'NOT PRESENT'
        print(f'var_check: NOT PRESENT')
        return self.checks['var_check']

    def check_var_has_coords(self, coords):
        """
            Check if the variable ID has coordinates
        :param coords: list of coords for example ["time", "lat", "lon"]
        :return: 'checks' dictionary with a result
        """
        files_found = glob.glob(self.path + '/*.nc')
        try:
            var_id = _get_var_id(files_found)
        except IndexError:
            return None

        ds = open_mfdatasets(files_found)
        a = set(list(ds[var_id].indexes.keys()))
        if a.issubset(coords):
            self.checks['coords_check'] = 'GOOD'
            print(f'coords_check: GOOD')
            return self.checks['coords_check']
        self.checks['coords_check'] = 'WRONG DIMENSIONS', a
        print(f'coords_check: WRONG DIMENSIONS')
        return self.checks['coords_check']

    def check_lat_in_range(self, lower_bnd, upper_bnd):
        """
            Check range of latitude
        :param lower_bnd: lower bound latitude
        :param upper_bnd: upper bound latitude
        :return: 'checks' dictionary with a result
        """
        files_found = glob.glob(self.path + '/*.nc')
        ds = open_mfdatasets(files_found)
        try:
            result = is_in_range(ds, 'lat', lower_bnd, upper_bnd)
        except TypeError:
            return None
        print(result)
        if result is True:
            self.checks['latitude_check'] = 'GOOD'
            print(f'latitude_check: GOOD')
            return self.checks['latitude_check']
        self.checks['latitude_check'] = 'INCORRECT RANGE', (lower_bnd, upper_bnd)
        print(f'latitude_check: INCORRECT RANGE')
        return self.checks['latitude_check']

    def check_lon_in_range(self, lower_bnd, upper_bnd):
        """
            Check range of longitude
        :param lower_bnd: lower bound longitude
        :param upper_bnd: upper bound longitude
        :return: 'checks' dictionary with a result
        """
        files_found = glob.glob(self.path + '/*.nc')
        ds = open_mfdatasets(files_found)
        try:
            result = is_in_range(ds, 'lon', lower_bnd, upper_bnd)
        except TypeError:
            return None
        if result:
            self.checks['longitude_check'] = 'GOOD'
            print(f'longitude_check: GOOD')
            return self.checks['longitude_check']
        self.checks['longitude_check'] = 'INCORRECT RANGE', (lower_bnd, upper_bnd)
        print(f'longitude_check: INCORRECT RANGE')
        return self.checks['longitude_check']

    def return_tuple_result(self):
        """
        :return: Tuple(number of issues found, dictionary of results)
        """
        num_issues = 0
        for results in self.checks.values():
            if not results == 'GOOD':
                num_issues += 1
        tuple_result = (num_issues, self.checks)
        return tuple_result
def main():
    a = Characterise('/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/seaIce/day/r1i1p1/v20110113')
    # a.check_path()
    b = Characterise(
        '/home/pmarek/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/seaIce/day/r1i1p1/v20110113/sic')
    # b.check_varnames()
    # b.check_var_in_file()
    # b.check_var_has_coords(["time", "lat", "lon"])
    b.check_lat_in_range(1, 90.5)
    # b.check_lon_in_range(0, 360)
    print(b.return_tuple_result())


if __name__=='__main__':
    main()