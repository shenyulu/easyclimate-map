# -*- coding: utf-8 -*-
"""
zh-CN First-Level Administration Centers
===================================

Import ``easyclimate-map`` for loading China first-level administration centers, matplotlib.pyplot for plotting, and cartopy.crs for map projections.
These libraries together support the retrieval and visualization of geographic data.
"""
import easyclimate_map as eclmap
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# %%
# Points
# -----------------
# Use ``easyclimate_map.get_zh_CN_1st_administration()`` to retrieve the point-type GeoDataFrame of China's first-level administration centers.
# This data includes provincial-level government seats and can be used to mark capital locations.
zh_provinces_line = eclmap.get_zh_CN_provinces(type = "line")
zh_admin1_points = eclmap.get_zh_CN_1st_administration()
zh_admin1_points

# %%
# Use GeoPandas' plot() method for quick visualization of the point locations.
# This step is for initial data inspection without custom projections.
zh_admin1_points.plot()

# %%
# Create a subplot with PlateCarree projection (central longitude 180°), set geographic extent [70-140°E, 0-50°N].
# Add gridlines, coastlines, China's national boundary line geometries (red lines, no fill), and administration center points (blue markers).
# This step demonstrates point overlays for administrative centers on top of national boundaries.
# Parameter Details:
#
# - set_extent: Defines the map display range.
# - gridlines: Adds latitude/longitude grid with labels.
# - coastlines: Draws global coastlines (50m resolution).
# - add_geometries: Overlays national boundaries with red edges, line width 0.3.
# - scatter: Plots administration centers with blue markers.
fig, ax = plt.subplots(subplot_kw={"projection": ccrs.PlateCarree(central_longitude=180)})

ax.set_extent([70, 140, 0, 50])
ax.gridlines(
    draw_labels=["left", "bottom"],
    color="grey",
    alpha=0.5, linestyle="--"
)
ax.coastlines(color="k", lw = 0.5, resolution = "50m")
ax.add_geometries(
    zh_provinces_line.geometry,
    crs = ccrs.PlateCarree(),
    facecolor = "none",
    edgecolor = "r",
    lw = 0.3
)
ax.scatter(
    zh_admin1_points.geometry.x,
    zh_admin1_points.geometry.y,
    s = 12,
    color = "b",
    transform = ccrs.PlateCarree()
)
