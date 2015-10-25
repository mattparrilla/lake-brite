import numpy as np
import scipy
import scipy.interpolate as inter
import matplotlib.pyplot as plt


def extrapolate_nans(x, y, v):
    """
    Extrapolate the NaNs or masked vals in a grid INPLACE using nearest
    value.

    .. warning:: Replaces the NaN or masked vals of the original array!

    Parameters:

    * x, y : 1D arrays
        Arrays with the x and y coordinates of the data points.
    * v : 1D array
        Array with the scalar value assigned to the data points.

    Returns:

    * v : 1D array
        The array with NaNs or masked vals extrapolated.
    """

    if np.ma.is_masked(v):
        nans = v.mask
    else:
        nans = np.isnan(v)
    notnans = np.logical_not(nans)
    v[nans] = scipy.interpolate.griddata((x[notnans], y[notnans]), v[notnans],
        (x[nans], y[nans]), method='nearest').ravel()
    return v

data = [
    {
        'station': 51,
        'coords': [1, 9],
        'value': 30
    }, {
        'station': 50,
        'coords': [2, 7],
        'value': 20
    }, {
        'station': 46,
        'coords': [4, 4],
        'value': 30
    }, {
        'station': 40,
        'coords': [10, 8],
        'value': 40
    }, {
        'station': 36,
        'coords': [11, 2],
        'value': 10
    }, {
        'station': 33,
        'coords': [14, 0],
        'value': 2
    }, {
        'station': 34,
        'coords': [14, 6],
        'value': 25
    }, {
        'station': 25,
        'coords': [17, 4],
        'value': 3
    }, {
        'station': 19,
        'coords': [21, 3],
        'value': 5
    }, {
        'station': 21,
        'coords': [21, 5],
        'value': 10
    }, {
        'station': 16,
        'coords': [23, 6],
        'value': 8
    }, {
        'station': 9,
        'coords': [30, 3],
        'value': 7
    }, {
        'station': 7,
        'coords': [34, 0],
        'value': 10
    }, {
        'station': 4,
        'coords': [40, 0],
        'value': 15
    }, {
        'station': 2,
        'coords': [48, 0],
        'value': 25
    }
]

vals = np.array([station['value'] for station in data])
pts = [station['coords'] for station in data]
grid_x, grid_y = np.mgrid[0:49:50j, 0:9:10j]
grid_z = inter.griddata(pts, vals, (grid_x, grid_y), method='cubic')

print "vals: "
print vals
print "pts: "
print pts
print "grid_x:"
print grid_x
print "grid_y:"
print grid_y
print "grid_z:"
print grid_z
x = []
y = []
for i in pts:
    x.append(i[0])
    y.append(i[1])

extrapolate_nans(grid_x, grid_y, grid_z)
plt.matshow(grid_z)
plt.show()
