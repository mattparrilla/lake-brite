from PIL import Image
from numpy import asarray

matrix = []
for i in range(0, 10):
    matrix.append([])
    for j in range(0, 15):
        matrix[i].append([])
        for k in range(0, 50):
            if i == j:
                matrix[i][j].append((k * 5, 0, 0))
            else:
                matrix[i][j].append((0, 0, 0))

for i, frame in enumerate(matrix):
    Image.fromarray(asarray(matrix[i], 'uint8')).show()
