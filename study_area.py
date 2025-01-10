import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.contour import QuadContourSet
from matplotlib.collections import QuadMesh
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.crs as ccrs
from cartopy.io.shapereader import BasicReader
import cmaps

from add_equal_axes import *
from find_side import *
from lambert_ticks import *
from mark_inset import *
from read_data import *

def add_geometries(ax: plt.Axes, provinces: BasicReader, countries: BasicReader) -> None:
    """
    Add provincial and national boundaries to a given subplot.

    Parameters:
    -----------
    ax : matplotlib.axes._axes.Axes
        The axis object to which geometries will be added.
    provinces : cartopy.io.shapereader.BasicReader
        Reader object for provincial boundary shapefiles.
    countries : cartopy.io.shapereader.BasicReader
        Reader object for national boundary shapefiles.

    Returns:
    --------
    None
    """
    ax.add_geometries(provinces.geometries(), linewidth=0.5, edgecolor='black', crs=ccrs.PlateCarree(), facecolor='none')
    ax.add_geometries(countries.geometries(), linewidth=1.0, edgecolor='black', crs=ccrs.PlateCarree(), facecolor='none')

def configure_gridlines(ax: plt.Axes, xticks: list[int], yticks: list[int]) -> None:
    """
    Configure gridlines and tick labels for a given subplot.

    Parameters:
    -----------
    ax : matplotlib.axes._axes.Axes
        The axis object for which gridlines and ticks are configured.
    xticks : list of int
        Longitude tick locations.
    yticks : list of int
        Latitude tick locations.

    Returns:
    --------
    None
    """
    ax.figure.canvas.draw()  # Automatically retrieve the figure from the axis and force a redraw
    ax.gridlines(xlocs=xticks, ylocs=yticks, draw_labels=False, linewidth=0.8, color='k', alpha=0.6, linestyle='--')
    ax.xaxis.set_major_formatter(LONGITUDE_FORMATTER)
    ax.yaxis.set_major_formatter(LATITUDE_FORMATTER)
    lambert_xticks(ax, xticks)
    lambert_yticks(ax, yticks)

def draw_d02_boundary(ax: plt.Axes, lon_1: np.ndarray, lat_1: np.ndarray) -> None:
    """
    Draw the boundary of the d02 simulation region on the given subplot.

    Parameters:
    -----------
    ax : matplotlib.axes._axes.Axes
        The axis object on which the boundary will be drawn.
    lon_1 : numpy.ndarray
        2D array of longitudes for the d02 region.
    lat_1 : numpy.ndarray
        2D array of latitudes for the d02 region.

    Returns:
    --------
    None
    """
    corners = [
        (lon_1[0, 0], lat_1[0, 0]), 
        (lon_1[-1, 0], lat_1[-1, 0]), 
        (lon_1[-1, -1], lat_1[-1, -1]), 
        (lon_1[0, -1], lat_1[0, -1]), 
        (lon_1[0, 0], lat_1[0, 0])
    ]
    ax.plot(*zip(*corners), color='k', lw=1.75, transform=ccrs.PlateCarree())

def plot_domain(ax: plt.Axes, lon: np.ndarray, lat: np.ndarray, hgt: np.ndarray, 
                xticks: list[int], yticks: list[int], 
                provinces: BasicReader, countries: BasicReader, 
                cmap: plt.cm.ScalarMappable, title: str, 
                use_pcolormesh: bool = False) -> Union[QuadContourSet, QuadMesh]:
    """
    Plot a domain with topography, gridlines, and geographic boundaries using either contourf or pcolormesh.

    Parameters:
    -----------
    ax : matplotlib.axes._axes.Axes
        The axis object where the domain will be plotted.
    lon : numpy.ndarray
        2D array of longitudes for the domain.
    lat : numpy.ndarray
        2D array of latitudes for the domain.
    hgt : numpy.ndarray
        2D array of terrain heights for the domain.
    xticks : list of int
        Longitude tick locations.
    yticks : list of int
        Latitude tick locations.
    provinces : cartopy.io.shapereader.BasicReader
        Reader object for provincial boundary shapefiles.
    countries : cartopy.io.shapereader.BasicReader
        Reader object for national boundary shapefiles.
    cmap : matplotlib.colors.Colormap
        Colormap for the terrain heights.
    title : str
        Title of the subplot.
    use_pcolormesh : bool, optional
        If True, use pcolormesh for plotting. If False, use contourf. Default is False.

    Returns:
    --------
    Union[matplotlib.contour.QuadContourSet, matplotlib.collections.QuadMesh]
        The plot object created by either contourf or pcolormesh.
    """
    hgt_min, hgt_max = np.nanmin(hgt), np.nanmax(hgt)
    if hgt_max > 5000 and hgt_min < 0:
        extend = 'both'
    elif hgt_max > 5000:
        extend = 'max'
    elif hgt_min < 0:
        extend = 'min'
    else:
        extend = None

    if use_pcolormesh:
        levels = np.arange(0, 5000 + 100, 100)
        norm = BoundaryNorm(levels, ncolors=cmap.N, extend=extend)
        mesh = ax.pcolormesh(lon, lat, hgt, transform=ccrs.PlateCarree(), cmap=cmap, norm=norm, shading='auto')
        plot_object = mesh
    else:
        contour = ax.contourf(
            lon, lat, hgt, transform=ccrs.PlateCarree(), cmap=cmap, 
            levels=np.arange(0, 5000 + 100, 100), extend=extend
        )
        plot_object = contour

    # Add geographic boundaries and gridlines
    add_geometries(ax, provinces, countries)
    configure_gridlines(ax, xticks, yticks)

    # Set title
    ax.set_title(title)

    return plot_object


if __name__ == "__main__":

    lon, lat, proj, hgt, lon_1, lat_1, hgt_1 = process_data(path='/data8/huangty/cn_WRF/2019_wps/')

    fig = plt.figure(figsize=(28, 12), dpi=200)
    plt.tight_layout()

    provinces = BasicReader('/data6/huangty/NCL-Chinamap-master/cnmap/cnmap.shp')
    countries = BasicReader('/data6/huangty/NCL-Chinamap-master/cnmap/cnhimap.shp')
    cmap = cmaps.MPL_terrain

    ax = fig.add_axes([0.09, 0.15, 0.4, 0.7], projection=proj)
    contour = plot_domain(ax, lon, lat, hgt, [75, 90, 105, 120, 135], [10, 20, 30, 40, 50], provinces, countries, cmap, "Domain d01", use_pcolormesh=True)
    #  contour = plot_domain(ax, lon, lat, hgt, [75, 90, 105, 120, 135], [10, 20, 30, 40, 50], provinces, countries, cmap, "Domain d01")
    draw_d02_boundary(ax, lon_1, lat_1)

    ax_inset = add_equal_axes(ax, loc='right', pad=0.03, width=0.4, projection=proj)
    plot_domain(ax_inset, lon_1, lat_1, hgt_1, [100, 105, 110, 115, 120], [20, 25, 30, 35, 40], provinces, countries, cmap, "Domain d02", use_pcolormesh=True)
    #  plot_domain(ax_inset, lon_1, lat_1, hgt_1, [100, 105, 110, 115, 120], [20, 25, 30, 35, 40], provinces, countries, cmap, "Domain d02")

    cbar = plt.colorbar(contour, ax=[ax, ax_inset], orientation='horizontal', pad=0.1, shrink=0.8, aspect=30)
    cbar.set_label('Height (m)')

    mark_inset(ax, ax_inset, loc1a=2, loc1b=1, loc2a=3, loc2b=4, fc="none", ec='k', lw=0.75)
    plt.savefig("WRF_domain.png")
