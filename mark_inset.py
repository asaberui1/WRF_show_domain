from typing import Tuple
from matplotlib.axes import Axes
from matplotlib.patches import Patch
from matplotlib.transforms import TransformedBbox
from mpl_toolkits.axes_grid1.inset_locator import TransformedBbox, BboxPatch, BboxConnector

def mark_inset(parent_axes: Axes, inset_axes: Axes, loc1a: int = 1, loc1b: int = 1, loc2a: int = 2, loc2b: int = 2, **kwargs) -> Tuple[Patch, Patch, Patch]:
    """
    Connect an inset axes to a parent axes with lines and a rectangle.

    Parameters
    ----------
    parent_axes : Axes
        The parent axes.
    inset_axes : Axes
        The inset axes.
    loc1a, loc1b : int
        Locations of the first connecting line on the inset and parent axes.
    loc2a, loc2b : int
        Locations of the second connecting line on the inset and parent axes.
    **kwargs : dict
        Additional keyword arguments for the patches and connectors.

    Returns
    -------
    Tuple[Patch, Patch, Patch]
        A tuple containing the rectangle and the two connecting lines.
    """
    rect = TransformedBbox(inset_axes.viewLim, parent_axes.transData)
    rect_patch = BboxPatch(rect, fill=False, **kwargs)
    parent_axes.add_patch(rect_patch)

    connector1 = BboxConnector(inset_axes.bbox, rect, loc1=loc1a, loc2=loc1b, **kwargs)
    connector2 = BboxConnector(inset_axes.bbox, rect, loc1=loc2a, loc2=loc2b, **kwargs)
    inset_axes.add_patch(connector1)
    inset_axes.add_patch(connector2)

    connector1.set_clip_on(False)
    connector2.set_clip_on(False)

    return rect_patch, connector1, connector2

