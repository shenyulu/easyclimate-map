"""
pytest for src\easyclimate_map\map\map_tibetan_plateau.py
"""

import pytest

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import easyclimate_map as eclmap


@pytest.mark.mpl_image_compare(remove_text=True, tolerance=20)
def test_get_Tibetan_Plateau_basins():
    tp_basins = eclmap.get_Tibetan_Plateau_basins()

    fig, ax = plt.subplots()
    tp_basins.plot(ax=ax)
    return fig
