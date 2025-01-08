import numpy as np
import cartopy.crs as ccrs
from netCDF4 import Dataset
from wrf import getvar, get_cartopy
from concurrent.futures import ThreadPoolExecutor
from typing import Tuple

def get_data(file: str) -> Tuple[np.ndarray, np.ndarray, ccrs.Projection, np.ndarray]:
    """
    Extract longitude, latitude, projection, and height data from a WRF NetCDF file.

    Parameters
    ----------
    file : str
        Path to the NetCDF file.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray, ccrs.Projection, np.ndarray]
        Longitude, latitude, projection, and height arrays.
    """
    with Dataset(file) as f:
        lon = getvar(f, 'lon', meta=False).data
        lat = getvar(f, 'lat', meta=False).data
        proj = get_cartopy(wrfin=f)
        hgt = getvar(f, 'HGT_M', meta=False).data
        hgt = np.maximum(hgt, 0)  # Ensure no negative values in height

    return lon, lat, proj, hgt

def process_data(path: str) -> Tuple[np.ndarray, np.ndarray, ccrs.Projection, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Process data from two files in parallel to retrieve coordinates and height information.

    Parameters
    ----------
    path : str
        Path to the geo_em directory.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray, ccrs.Projection, np.ndarray, np.ndarray, np.ndarray, np.ndarray]
        A tuple containing longitude, latitude, projection, height for two datasets.
    """
    file_d01 = path + '/geo_em.d01.nc'
    file_d02 = path + '/geo_em.d02.nc'

    with ThreadPoolExecutor() as executor:
        future_d01 = executor.submit(get_data, file_d01)
        future_d02 = executor.submit(get_data, file_d02)

        lon, lat, proj, hgt = future_d01.result()
        lon_1, lat_1, _, hgt_1 = future_d02.result()

    return lon, lat, proj, hgt, lon_1, lat_1, hgt_1
