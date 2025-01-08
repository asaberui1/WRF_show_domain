from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.transforms import Bbox
from typing import Union
import cartopy.crs as ccrs
import numpy as np

def add_equal_axes(ax: Union[Axes, np.ndarray], loc: str, pad: float, width: float, projection: ccrs.Projection = None) -> Axes:
    """
    Add a new axes adjacent to an existing one with equal height or width.

    Parameters
    ----------
    ax : Union[Axes, np.ndarray]
        The original axes or an array of axes.
    loc : str
        Position of the new axes relative to the original ('left', 'right', 'bottom', 'top').
    pad : float
        Spacing between the original and new axes.
    width : float
        Width of the new axes (if 'left' or 'right') or height (if 'bottom' or 'top').
    projection : ccrs.Projection, optional
        The cartopy projection for the new axes.

    Returns
    -------
    Axes
        The newly created axes.
    """
    axes = np.atleast_1d(ax).ravel()
    bbox = Bbox.union([ax.get_position() for ax in axes])

    if loc == 'left':
        x0_new = bbox.x0 - pad - width
        x1_new = bbox.x0 - pad
        y0_new, y1_new = bbox.y0, bbox.y1
    elif loc == 'right':
        x0_new = bbox.x1 + pad
        x1_new = bbox.x1 + pad + width
        y0_new, y1_new = bbox.y0, bbox.y1
    elif loc == 'bottom':
        x0_new, x1_new = bbox.x0, bbox.x1
        y0_new = bbox.y0 - pad - width
        y1_new = bbox.y0 - pad
    elif loc == 'top':
        x0_new, x1_new = bbox.x0, bbox.x1
        y0_new = bbox.y1 + pad
        y1_new = bbox.y1 + pad + width
    else:
        raise ValueError("Invalid location. Choose from 'left', 'right', 'bottom', or 'top'.")

    fig: Figure = axes[0].get_figure()
    new_bbox = Bbox.from_extents(x0_new, y0_new, x1_new, y1_new)
    ax_new = fig.add_axes(new_bbox, projection=projection)

    return ax_new

