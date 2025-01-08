import numpy as np
import cartopy.crs as ccrs
import shapely.geometry as sgeom
from typing import List, Tuple
from find_side import *

def _lambert_ticks(ax, ticks: List[float], tick_location: str, line_constructor, tick_extractor) -> Tuple[List[float], List[float]]:
    """
    Get the tick locations and labels for an axis of a Lambert Conformal projection.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes of the plot on which the Lambert Conformal projection is applied.

    ticks : List[float]
        A list of values representing the desired tick positions on the axis (either x or y).

    tick_location : str
        The location of the ticks on the axis. Can be either 'left' or 'bottom'.
    
    line_constructor : callable
        A function that generates a line of coordinates given a tick position. 
        It takes a tick value and returns a line (array of coordinates) on the projection.

    tick_extractor : callable
        A function that extracts tick locations from the intersection points of the line and the projection boundary.
        It takes the intersection points as input and returns the tick locations.

    Returns
    -------
    Tuple[List[float], List[float]]
        A tuple containing:
        - A list of tick locations in the map projection.
        - A list of corresponding tick labels.

    Notes
    -----
    This function determines the tick locations and labels based on the intersection of the desired ticks
    with the projection boundary, ensuring that only visible ticks are returned.
    """
    # Ensure the tick_location is valid
    valid_locations = ['left', 'bottom']
    if tick_location not in valid_locations:
        raise ValueError(f"Invalid tick_location: {tick_location}. Must be one of {valid_locations}.")

    # Extract the boundary of the axes (bounding box) in geodetic coordinates
    outline_patch = sgeom.LineString(ax.spines['geo'].get_path().vertices.tolist())
    axis = find_side(outline_patch, tick_location)
    
    # Number of steps used to evaluate ticks
    n_steps = 30
    extent = ax.get_extent(ccrs.PlateCarree())
    
    # List to hold the final tick positions and labels
    tick_locations = []
    tick_labels = ticks.copy()

    for tick in ticks:
        # Generate the line corresponding to this tick using the line_constructor
        xy = line_constructor(tick, n_steps, extent)
        
        # Project the coordinates into map projection space
        proj_xyz = ax.projection.transform_points(ccrs.Geodetic(), xy[:, 0], xy[:, 1])
        xyt = proj_xyz[..., :2]
        
        # Create a Shapely LineString for the projected coordinates
        line = sgeom.LineString(xyt.tolist())
        
        # Get the intersection points between the axis and the projected line
        locs = axis.intersection(line)
        
        # Extract the tick location from the intersection points
        tick_location = tick_extractor(locs.xy) if locs else [None]
        
        # Append the tick location
        tick_locations.append(tick_location[0])

    # Remove ticks that are not visible (None values)
    visible_ticks = [(tick, label) for tick, label in zip(tick_locations, tick_labels) if tick is not None]
    tick_locations, tick_labels = zip(*visible_ticks) if visible_ticks else ([], [])

    return list(tick_locations), list(tick_labels)

def lambert_xticks(ax, ticks: List[float]) -> None:
    """
    Draw ticks on the bottom x-axis of a Lambert Conformal projection.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes of the plot with a Lambert Conformal projection.

    ticks : List[float]
        A list of longitude values to be used as tick positions along the bottom x-axis.

    Returns
    -------
    None
        Modifies the axes in place by adding the ticks and their labels.
    """
    def extract_x(xy):
        """Extract the x-coordinate from the intersection point."""
        return xy[0]

    def construct_line(t, n_steps, extent):
        """
        Construct a vertical line (longitude) for the given tick value.
        """
        return np.vstack((np.full(n_steps, t), np.linspace(extent[2], extent[3], n_steps))).T

    # Get tick locations and labels using the helper function
    xtick_positions, xtick_labels = _lambert_ticks(ax, ticks, 'bottom', construct_line, extract_x)

    # Set the ticks and labels on the bottom axis
    ax.xaxis.tick_bottom()
    ax.set_xticks(xtick_positions)
    ax.set_xticklabels([ax.xaxis.get_major_formatter()(xtick) for xtick in xtick_labels])

def lambert_yticks(ax, ticks: List[float]) -> None:
    """
    Draw ticks on the left y-axis of a Lambert Conformal projection.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes of the plot with a Lambert Conformal projection.

    ticks : List[float]
        A list of latitude values to be used as tick positions along the left y-axis.

    Returns
    -------
    None
        Modifies the axes in place by adding the ticks and their labels.
    """
    def extract_y(xy):
        """Extract the y-coordinate from the intersection point."""
        return xy[1]

    def construct_line(t, n_steps, extent):
        """
        Construct a horizontal line (latitude) for the given tick value.
        """
        return np.vstack((np.linspace(extent[0], extent[1], n_steps), np.full(n_steps, t))).T

    # Get tick locations and labels using the helper function
    ytick_positions, ytick_labels = _lambert_ticks(ax, ticks, 'left', construct_line, extract_y)

    # Set the ticks and labels on the left axis
    ax.yaxis.tick_left()
    ax.set_yticks(ytick_positions)
    ax.set_yticklabels([ax.yaxis.get_major_formatter()(ytick) for ytick in ytick_labels])
