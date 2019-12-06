"""
Tests for xarray datasets.
"""

import xarray as xr

from dataset_utils import *


def _good_dataset():
    return xr.open_dataset('/badc/ecmwf-era-interim/data/gg/ap/2000/01/01/ggap200001010000.nc')


def test_has_variables_success():
    ds = _good_dataset()

    variables = set(ds.data_vars)
    expected = set(['Z', 'T', 'W', 'STRF', 'VPOT', 'U', 'V', 'R', 'VO', 'D', 'PV', 'Q', 'O3', 'CLWC', 'CIWC', 'CC'])
    assert(variables == expected)


def test_has_variables_fail_wrong_vars():
    ds = _good_dataset()

    variables = set(ds.data_vars)
    expected = set(['rubbish', 'nodata'])
    assert(variables != expected)

    
