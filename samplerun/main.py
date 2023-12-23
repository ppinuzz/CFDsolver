# ------------ SAMPLE RUN OF THE CFD SOLVER ------------

from pycfd.pymesh import pymesh
import matplotlib.pyplot as plt
import numpy as np


geo_file = 'geometry.input'
mesh_file = 'sample.mesh'
discretisation = 'FD'

pymesh.mesher(geo_file, mesh_file, discretisation)

mesh = pymesh.read_mesh(mesh_file)


# ------------ VISUALISATION ------------

x_plot = np.zeros(len(mesh))

plt.figure()
plt.plot(x_plot, mesh)
plt.show()