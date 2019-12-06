import xarray as xr
import os
from pathlib import Path
import glob


def has_coordinates(ds, coords):
    try:
        idx = list(ds.indexes.keys())
    except Exception:
        return False

    print(idx, coords)

    if not len(idx) >= len(coords):
        return False
    return all([i == j for i, j in zip(idx, coords)])


def has_variables(ds, variables):
    try:
        b = list(ds.data_vars.keys())
        c = set(variables)
        return c.issubset(b)
    except Exception:
        return False


def has_attribute(ds, variable, name, value, attr_type=None):
    try:
        attr = ds[variable].attrs
        if attr:
            result = attr['units']
            if result:
                return True
        return False
    except Exception:
        return False


def has_shape(ds, variable):
    try:
        result = ds[variable].shape
        if len(result) == 3:
            return True
        return False
    except Exception:
        return False


def is_in_range(ds, coord_variable, lower_bound, upper_bound, inclusive=True):
    try:
        lower_bnd = ds.coords[coord_variable].values[0]
        upper_bnd = ds.coords[coord_variable].values[-1]
        lower = lower_bound
        upper = upper_bound
        if lower_bnd <= lower and upper_bnd >= upper:
            return True
        return False
    except Exception:
        return False



def open_dataset(file_to_open):
    """
        :param file_to_open: netCDF4 files
        :return: opened netCDF dataset
    """
    try:
        with xr.open_dataset(file_to_open) as ds:
            return ds
    except Exception as e:
        return e

def main():
    fpath = 'xarray'
    absolute_path = os.path.join(str(Path.home()), fpath)
    files = glob.glob(absolute_path + '/tas_Amon*.nc')

    opened = open_dataset(files[0])
    print(has_coordinates(opened, ['time', 'lat', 'lon']))


if __name__=='__main__':
    main()