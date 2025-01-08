import shapely.geometry as sgeom

'''
Adapted from Andrew Dawson's method: https://gist.github.com/ajdawson/dd536f786741e987ae4e
'''

def find_side(line_string: sgeom.LineString, side: str) -> sgeom.LineString:
    """
    Given a shapely LineString that is assumed to be rectangular, return the line 
    corresponding to a given side of the rectangle.

    Parameters
    ----------
    line_string : shapely.geometry.LineString
        A `LineString` object representing the boundary of the rectangle.
    
    side : str
        The side of the rectangle to retrieve. Valid values are:
        - 'left' : Returns the left vertical line of the rectangle.
        - 'right' : Returns the right vertical line of the rectangle.
        - 'bottom' : Returns the bottom horizontal line of the rectangle.
        - 'top' : Returns the top horizontal line of the rectangle.

    Returns
    -------
    shapely.geometry.LineString
        A `LineString` object representing the corresponding side of the rectangle.

    Raises
    ------
    ValueError
        If the `side` argument is not one of the valid values ('left', 'right', 'bottom', 'top').
    """
    # Ensure the side is valid
    valid_sides = ['left', 'right', 'bottom', 'top']
    if side not in valid_sides:
        raise ValueError(f"Invalid side: {side}. Must be one of {valid_sides}.")

    # Extract the bounds of the LineString
    minx, miny, maxx, maxy = line_string.bounds

    # Define the coordinates for each side of the rectangle
    side_points = {
        'left': [(minx, miny), (minx, maxy)],
        'right': [(maxx, miny), (maxx, maxy)],
        'bottom': [(minx, miny), (maxx, miny)],
        'top': [(minx, maxy), (maxx, maxy)],
    }

    # Return the corresponding side as a LineString
    return sgeom.LineString(side_points[side])

