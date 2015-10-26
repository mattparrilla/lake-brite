import numpy as np
import scipy
import scipy.interpolate as inter
import matplotlib.pyplot as plt
from lake_clip import clip_data_to_lake


# def extrapolate_nans(x, y, v):
#     """
#     Extrapolate the NaNs or masked vals in a grid INPLACE using nearest
#     value.
# 
#     .. warning:: Replaces the NaN or masked vals of the original array!
# 
#     Parameters:
# 
#     * x, y : 1D arrays
#         Arrays with the x and y coordinates of the data points.
#     * v : 1D array
#         Array with the scalar value assigned to the data points.
# 
#     Returns:
# 
#     * v : 1D array
#         The array with NaNs or masked vals extrapolated.
#     """
# 
#     # TODO: make the 3rd argument of
#     if np.ma.is_masked(v):
#         nans = v.mask
#     else:
#         nans = np.isnan(v)
#     notnans = np.logical_not(nans)
# 
#     x_edge_nans = []
#     y_edge_nans = []
#     for index, i in enumerate(np.nditer(x[nans])):
#         j = y[nans][index]
#         if i == 0. or i == 49. or j == 0. or j == 9.:
#             x_edge_nans.append(x[nans][index])
#             y_edge_nans.append(j)
# 
#     v[nans][0:81] = scipy.interpolate.griddata((x[notnans], y[notnans]), v[notnans],
#         (np.array(x_edge_nans), np.array(y_edge_nans)), method='nearest').ravel()
#     return v


data = [
    {
        'station': 51,
        'coords': [1, 9],
        'value': 9.3
    }, {
        'station': 50,
        'coords': [2, 7],
        'value': 13
    }, {
        'station': 40,
        'coords': [10, 8],
        'value': 18.7
    }, {
        'station': 34,
        'coords': [14, 6],
        'value': 7.2
    }, {
        'station': 46,
        'coords': [4, 4],
        'value': 7.5
    }, {
        'station': 36,
        'coords': [11, 2],
        'value': 10.1
    }, {
        'station': 33,
        'coords': [14, 0],
        'value': 12.4
    }, {
        'station': 25,
        'coords': [17, 4],
        'value': 8.1
    }, {
        'station': 19,
        'coords': [21, 3],
        'value': 6.5
    }, {
        'station': 21,
        'coords': [21, 5],
        'value': 6.5
    }, {
        'station': 16,
        'coords': [23, 6],
        'value': 8.7
    }, {
        'station': 9,
        'coords': [30, 3],
        'value': 9.4
    }, {
        'station': 7,
        'coords': [34, 0],
        'value': 6.5
    }, {
        'station': 4,
        'coords': [40, 0],
        'value': 28
    }, {
        'station': 2,
        'coords': [48, 0],
        'value': 13.1
    }
]


# def inpaint_nans(im):
#     ipn_kernel = np.array([[1,1,1],[1,0,1],[1,1,1]]) # kernel for inpaint_nans
#     nans = np.isnan(im)
#     while np.sum(nans)>0:
#         im[nans] = 0
#         vNeighbors = scipy.signal.convolve2d((nans==False),ipn_kernel,mode='same',boundary='symm')
#         im2 = scipy.signal.convolve2d(im,ipn_kernel,mode='same',boundary='symm')
#         im2[vNeighbors>0] = im2[vNeighbors>0]/vNeighbors[vNeighbors>0]
#         im2[vNeighbors==0] = np.nan
#         im2[(nans==False)] = im[(nans==False)]
#         im = im2
#         nans = np.isnan(im)
#     return im


def nearest_neighbor(data):
    """Given lake station data, calculate nearest neighbor for every point
       in the 2D array of the display. Returns the 2D array"""
    vals = np.array([station['value'] for station in data])
    pts = [station['coords'] for station in data]
    grid_x, grid_y = np.mgrid[0:49:50j, 0:9:10j]
    grid_z = inter.griddata(pts, vals, (grid_x, grid_y), method='nearest')
    return grid_z

data = nearest_neighbor(data)
plt.matshow(data)
plt.show()
