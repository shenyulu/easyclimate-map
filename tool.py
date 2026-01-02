"""
Utility
"""
import py7zr
import geopandas as gpd
import tempfile
import os

from geopandas import GeoDataFrame

__all__ = ["read_shapefile_from_7z"]

def read_shapefile_from_7z(filepath: str, **kwargs) -> GeoDataFrame:
    """
    Read a shapefile directly from a 7z archive without extracting to disk.
    
    This function extracts a shapefile from a compressed 7z archive into a temporary
    directory, loads it as a GeoDataFrame using GeoPandas, and returns the result.
    All keyword arguments are passed through to `gpd.read_file()`.
    
    Parameters
    ----------
    filepath : str
        Path to the 7z archive containing the shapefile.
    **kwargs : dict, optional
        Additional keyword arguments to pass to `gpd.read_file()`.
        Common arguments include:
        - bbox : tuple
            Filter by bounding box (minx, miny, maxx, maxy)
        - mask : geometry
            Filter by geometry mask
        - rows : int
            Number of rows to read
        - encoding : str
            File encoding (e.g., 'utf-8')
        - driver : str
            GDAL/OGR driver name
    
    Returns
    -------
    geopandas.GeoDataFrame
        A GeoDataFrame containing the shapefile data.
    
    Raises
    ------
    FileNotFoundError
        If the 7z file doesn't exist or doesn't contain any .shp files.
    
    Notes
    -----
    - The function creates a temporary directory that is automatically cleaned up.
    - Only the first .shp file found in the archive will be read.
    - Shapefile companion files (.shx, .dbf, .prj) must also be present in the archive.
    
    Examples
    --------
    >>> gdf = read_shapefile_from_7z('data.7z')
    >>> gdf = read_shapefile_from_7z('data.7z', bbox=(xmin, ymin, xmax, ymax))
    >>> gdf = read_shapefile_from_7z('data.7z', encoding='utf-8', rows=1000)
    
    See Also
    --------
    geopandas.read_file : For available keyword arguments and reading options.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Extract the entire archive to temporary directory
        with py7zr.SevenZipFile(filepath, 'r') as archive:
            archive.extractall(path=tmpdir)
        
        # Find .shp files in the extracted contents
        shp_files = [f for f in os.listdir(tmpdir) if f.endswith('.shp')]
        
        if not shp_files:
            raise FileNotFoundError("No .shp file found in the 7z archive")
        
        # Read the shapefile using GeoPandas
        shp_path = os.path.join(tmpdir, shp_files[0])
        gdf = gpd.read_file(shp_path, **kwargs)
    
    return gdf
