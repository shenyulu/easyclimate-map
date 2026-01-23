"""
pytest for src\easyclimate_map\map\map_zh_CN.py
"""

import pytest

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import easyclimate_map as eclmap


@pytest.mark.mpl_image_compare(remove_text=True, tolerance=20)
def test_get_zh_CN_nation_line():
    zh_border_line = eclmap.get_zh_CN_nation(type = "line")

    fig, ax = plt.subplots()
    zh_border_line.plot(ax = ax)
    return fig

@pytest.mark.mpl_image_compare(remove_text=True, tolerance=20)
def test_get_zh_CN_nation_polygon():
    zh_border_polygon = eclmap.get_zh_CN_nation(type = "polygon")

    fig, ax = plt.subplots()
    zh_border_polygon.plot(ax = ax)
    return fig

@pytest.mark.mpl_image_compare(remove_text=True, tolerance=20)
def test_get_zh_CN_provinces_line():
    zh_provinces_line = eclmap.get_zh_CN_provinces(type = "line")

    fig, ax = plt.subplots()
    zh_provinces_line.plot(ax = ax)
    return fig

@pytest.mark.mpl_image_compare(remove_text=True, tolerance=20)
def test_get_zh_CN_provinces_polygon():
    zh_provinces_polygon = eclmap.get_zh_CN_provinces(type = "polygon")

    fig, ax = plt.subplots()
    zh_provinces_polygon.plot(ax = ax)
    return fig

@pytest.mark.mpl_image_compare(remove_text=True, tolerance=20)
def test_get_zh_CN_river1_line():
    zh_river1_line = eclmap.get_zh_CN_river1(type = "line")

    fig, ax = plt.subplots()
    zh_river1_line.plot(ax = ax)
    return fig

@pytest.mark.mpl_image_compare(remove_text=True, tolerance=20)
def test_get_zh_CN_river1_polygon():
    zh_river1_polygon = eclmap.get_zh_CN_river1(type = "polygon")

    fig, ax = plt.subplots()
    zh_river1_polygon.plot(ax = ax)
    return fig

@pytest.mark.mpl_image_compare(remove_text=True, tolerance=20)
def test_get_zh_CN_river3_line():
    zh_river3_line = eclmap.get_zh_CN_river3(type = "line")

    fig, ax = plt.subplots()
    zh_river3_line.plot(ax = ax)
    return fig

@pytest.mark.mpl_image_compare(remove_text=True, tolerance=20)
def test_get_zh_CN_river1_polygon():
    zh_river3_polygon = eclmap.get_zh_CN_river3(type = "polygon")

    fig, ax = plt.subplots()
    zh_river3_polygon.plot(ax = ax)
    return fig

@pytest.mark.mpl_image_compare(remove_text=True, tolerance=20)
def test_get_zh_CN_1st_administration():
    zh_CN_1st_administration = eclmap.get_zh_CN_1st_administration()

    fig, ax = plt.subplots()
    zh_CN_1st_administration.plot(ax = ax)
    return fig

@pytest.mark.mpl_image_compare(remove_text=True, tolerance=20)
def test_get_zh_CN_2nd_administration():
    zh_CN_2nd_administration = eclmap.get_zh_CN_2nd_administration()

    fig, ax = plt.subplots()
    zh_CN_2nd_administration.plot(ax = ax)
    return fig
