"""
Tests for xarray datasets.
"""
import pytest
from dataset_utils import *

fpath = 'badc/cmip5/data/cmip5/output1/MOHC/HadCM3/rcp45/mon/atmos/Amon/r1i1p1/latest/tas/tas_Amon_HadCM3_rcp45_r1i1p1_200601-203012.nc'
absolute_path = os.path.join(str(Path.home()), fpath)

def open_dataset(file):
    file_to_open = open_file(file)
    return file_to_open


def test_has_variables_success():
    ds = open_dataset(absolute_path)

    expected = set(['tas'])
    assert has_variables(ds, expected) is True

def test_has_variables_fail_wrong_vars():
    ds = open_dataset(absolute_path)

    expected = set(['rubbish', 'nodata'])
    expected2 = set([1, 2])
    assert has_variables(ds, expected) is False
    assert has_variables(ds, expected2) is False

def test_has_variables_raise_empty_list_exception():
    ds = open_dataset(absolute_path)

    expected = set([])
    with pytest.raises(ValueError):
        has_variables(ds, expected)

def test_has_coordinates_success():
    ds = open_dataset(absolute_path)

    expected = ['time', 'lat', 'lon']
    expected2 = ['time', 'lat']
    assert has_coordinates(ds, expected) is True
    assert has_coordinates(ds, expected2) is True

def test_has_coordinates_fail_wrong_coords():
    ds = open_dataset(absolute_path)

    expected = set(['rubbish', 'nodata'])
    expected2 = set(['time', 'lat', 'lon', 'nodata'])
    assert has_coordinates(ds, expected) is False
    assert has_coordinates(ds, expected2) is False

def test_has_coordinates_raise_empty_list_exception():
    ds = open_dataset(absolute_path)

    expected = set([])
    with pytest.raises(ValueError):
        has_coordinates(ds, expected)

def test_has_attribute_success():
    ds = open_dataset(absolute_path)

    assert has_attribute(ds, 'tas', 'K') is True

def test_has_attribute_fail_wrong_attribute():
    ds = open_dataset(absolute_path)

    assert has_attribute(ds, 'tas', 'J') is False
    assert has_attribute(ds, 1, 'rubbish') is False
    assert has_attribute(ds, ['tas', 'K'],'K') is False

def test_has_shape_success():
    ds = open_dataset(absolute_path)

    expected = 'tas'
    assert has_shape(ds, expected) is True

def test_has_shape_fail_wrong_variable():
    ds = open_dataset(absolute_path)

    expected = 'tasmax'
    expected2 = 0
    expected3 = ['rubbish', 0, 'nodata']
    assert has_shape(ds, expected) is False
    assert has_shape(ds, expected2) is False
    assert has_shape(ds, expected3) is False

def test_is_in_range_success():
    ds = open_dataset(absolute_path)

    assert is_in_range(ds, 'lat', -90, 90) is True
    assert is_in_range(ds, 'lon', 0, 360) is True

def test_is_in_range_fail_wrong_data():
    ds = open_dataset(absolute_path)

    assert is_in_range(ds, 'lat', -90.1, 91) is False
    assert is_in_range(ds, 'rubbish', [-70,90], 'nodata') is False
    assert is_in_range(ds, 'lon', -1, 360.01) is False