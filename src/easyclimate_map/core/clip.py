"""
Geospatial Clipping Utilities

This module provides functions for clipping and converting geospatial data
for visualization in matplotlib with cartopy projections. The tools are
specifically designed for working with GeoDataFrame objects and converting
them to matplotlib-compatible path objects for clipping operations.
"""

__all__ = [
    "get_geometry_path",
    "clip_rectangle_geometry",
]

import cartopy.crs as ccrs
import geopandas as gpd
import matplotlib.axes
from geopandas.geodataframe import GeoDataFrame
from ..core.datanode import DataNode


def get_geometry_path(
    gdf: GeoDataFrame,
    ax: matplotlib.axes.Axes,
) -> DataNode:
    """
    Convert geometries from a GeoDataFrame into matplotlib clipping paths.

    This function extracts geometries from a GeoDataFrame, projects them to
    the coordinate system of the given matplotlib axis, and converts them
    into matplotlib Path objects suitable for clipping or other operations.

    Parameters
    ----------
    gdf : :py:class:`geopandas.GeoDataFrame <geopandas.GeoDataFrame>`
        The GeoDataFrame containing geometries to be converted. Geometries
        should be in geographic coordinates (longitude/latitude in degrees)
        using the EPSG:4326 (PlateCarree) coordinate reference system.
    ax : :py:class:`matplotlib.axes.Axes`
        The matplotlib axis with a cartopy projection. The axis must have
        a cartopy.crs projection set, which will be used to transform the
        geometries from geographic coordinates to the map's coordinate system.

    Returns
    -------
    :py:class:`easyclimate-map.DataNode <easyclimate-map.core.datanode.DataNode>`

    A DataNode object containing two items:

    - clip_path: :py:class:`matplotlib.path.Path <matplotlib.path.Path>`
        A compound Path object containing all projected geometries.
    - transform_clip_path: :py:class:`matplotlib.transforms.TransformedPath <matplotlib.transforms.TransformedPath>`
        The same Path object transformed to data coordinates of the axis.

    Notes
    -----
    1. The function assumes input geometries are in geographic coordinates
       (EPSG:4326 / PlateCarree).
    2. The axis must use a cartopy projection. Standard matplotlib axes
       without cartopy will not work.
    3. The resulting Path objects can be used for clipping matplotlib plots
       or other operations that require vector paths.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> import cartopy.crs as ccrs
    >>> import geopandas as gpd
    >>>
    >>> # Create a map with cartopy projection
    >>> fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
    >>> # Load GeoDataFrame (assumed to be in geographic coordinates)
    >>> gdf = gpd.read_file('path/to/shapefile.shp')
    >>> # Convert geometries to clipping paths
    >>> paths = get_geometry_path(gdf, ax)
    >>> # Use the paths for clipping
    >>> im = ax.imshow(data, transform=ccrs.PlateCarree())
    >>> im.set_clip_path(paths['transform_clip_path'])

    See Also
    --------
    :py:func:`cartopy.mpl.path.shapely_to_path <cartopy.mpl.path.shapely_to_path>` : Converts shapely geometries to matplotlib paths
    :py:func:`matplotlib.path.Path.make_compound_path <matplotlib.path.Path.make_compound_path>` : Combines multiple paths into one
    :py:func:`matplotlib.transforms.TransformedPath <matplotlib.transforms.TransformedPath>` : Applies transformations to paths
    """
    from cartopy.mpl.path import shapely_to_path
    from matplotlib.path import Path
    import matplotlib.transforms as mt

    # Get the map projection for transforming geometries
    proj = ax.projection
    source_crs = ccrs.PlateCarree()  # Standard geographic CRS for shapefile

    path_list = list()
    for item in list(gdf["geometry"]):
        # Project each geometry to map coords (shifts lon appropriately)
        projected_item = proj.project_geometry(item, source_crs)
        tmp = shapely_to_path(projected_item)
        path_list.append(tmp)

    clip_path = Path.make_compound_path(*path_list)
    transform_clip_path = mt.TransformedPath(clip_path, transform=ax.transData)

    root = DataNode()
    root["clip_path"] = clip_path
    root["transform_clip_path"] = transform_clip_path
    return root


def clip_rectangle_geometry(
    gdf: GeoDataFrame,
    *args,
) -> GeoDataFrame:
    """
    Clip a GeoDataFrame using a rectangular bounding box.

    Supports two parameter styles:
    1. Four separate arguments: clip_rectangle_geometry(gdf, lon1, lon2, lat1, lat2)
    2. A single list/tuple: clip_rectangle_geometry(gdf, [lon1, lon2, lat1, lat2])

    Parameters
    ----------
    gdf : :py:class:`geopandas.GeoDataFrame <geopandas.GeoDataFrame>`
        The GeoDataFrame to clip
    *args : Union[float, List[float], Tuple[float]]
        Either four separate float arguments (lon1, lon2, lat1, lat2)
        or a single list/tuple containing four floats

    Returns
    -------
    :py:class:`geopandas.GeoDataFrame <geopandas.GeoDataFrame>`
        The clipped GeoDataFrame

    Examples
    --------
    >>> # Method 1: Four separate arguments
    >>> clipped = clip_rectangle_geometry(gdf, 110, 130, 30, 40)
    >>>
    >>> # Method 2: Single list argument
    >>> clipped = clip_rectangle_geometry(gdf, [110, 130, 30, 40])
    """
    from shapely.geometry import box

    # Extract coordinates from arguments
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        # Case: Single list/tuple argument
        coords = args[0]
        if len(coords) != 4:
            raise ValueError(
                f"List/tuple must contain exactly 4 values. "
                f"Received {len(coords)} values: {coords}"
            )
        x1, x2, y1, y2 = coords

    elif len(args) == 4:
        # Case: Four separate arguments
        x1, x2, y1, y2 = args

    else:
        raise ValueError(
            f"Invalid number of arguments. "
            f"Expected either 4 separate arguments or 1 list/tuple with 4 values. "
            f"Received {len(args)} arguments: {args}"
        )

    # Validate coordinate types
    for coord in (x1, x2, y1, y2):
        if not isinstance(coord, (int, float)):
            raise ValueError(
                f"All coordinates must be numeric values. "
                f"Received: {type(coord).__name__}"
            )

    # Determine bounding box coordinates (ensure min/max order)
    x_min = min(x1, x2)
    x_max = max(x1, x2)
    y_min = min(y1, y2)
    y_max = max(y1, y2)

    # Create bounding box geometry
    bbox = box(x_min, y_min, x_max, y_max)

    # Create GeoDataFrame for the bounding box
    bbox_gdf = gpd.GeoDataFrame(geometry=[bbox], crs=gdf.crs)

    # Perform clipping operation
    clipped_data = gpd.clip(gdf, bbox_gdf)

    return clipped_data
