import xarray as xr
import os
from pathlib import Path
import glob


def has_coordinates(ds, coords):
    """
        Check if given coordinates are included
        in a dataset

    :param ds: opened NetCDF4 file
    :param coords: list of coordinates like ['time', 'lat', 'lon']
    :return: Boolean
    """
    try:
        idx = list(ds.indexes.keys())
    except Exception:
        return False

    if not len(idx) >= len(coords):
        return False
    return all([i == j for i, j in zip(idx, coords)])


def has_variables(ds, variables):
    """
        Check if given variables are included
        in a dataset

    :param ds: opened NetCDF4 file
    :param variables: list of variables like ['tas', 'uas']
    :return: Boolean
    """
    try:
        b = list(ds.data_vars.keys())
    except Exception:
        return False

    c = set(variables)
    return c.issubset(b)


def has_attribute(ds, variable, value):
    """
        Check if a variable holds a
        desired value

    :param ds: opened NetCDF4 file
    :param variable: for example - 'tas'
    :param value: for example - 'K'
    :return: Boolean
    """
    try:
        attr = ds[variable].attrs
    except Exception:
        return False

    result = attr['units']
    if result == value and isinstance(result, str):
        return True
    return False



def has_shape(ds, variable):
    """
        Check if a variable has a shape

    :param ds: opened NetCDF4 file
    :param variable: for example - 'tas'
    :return: Boolean
    """
    try:
        result = ds[variable].shape
    except Exception:
        return False

    if len(result) == 3:
        return True
    return False


def is_in_range(ds, coord_variable, lower_bound, upper_bound):
    """
        Check for a given range of a coordinate

    :param ds: opened NetCDF4 file
    :param coord_variable: for example - 'lat'
    :param lower_bound: -80
    :param upper_bound: 90
    :return: Boolean
    """
    try:
        lower_bnd = ds.coords[coord_variable].values[0]
        upper_bnd = ds.coords[coord_variable].values[-1]
    except Exception:
        return False

    lower = lower_bound
    upper = upper_bound
    if lower_bnd <= lower and upper_bnd >= upper:
        return True
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
    # print(has_attribute(opened, 'tas', 'K'))
    # print(has_shape(opened, 'tas'))
    # print(is_in_range(opened, 'lat', -70, 90))
    # print(has_variables(opened, ['tas', 'tasmax']))
    print(has_coordinates(opened, ['time', 'lat', 'lon']))


if __name__=='__main__':
    main()
