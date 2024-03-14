#!/usr/bin/env python3

# add the path of the module to sys.path, otherwise Python won't find it...
# (https://docs.python-guide.org/writing/structure/#test-suite)
import context
# submodules are NOT imported by default, you have to import them explicitly
# (https://stackoverflow.com/a/8899345/17220538)
import pycfd.pymesh as pmsh
import matplotlib.pyplot as plt
import numpy as np


#%% PROVA

sample_folder = '../samplerun/'
geo_file = sample_folder + '/geometry.input'
mesh_file = sample_folder + 'sample.mesh'
discretisation = 'FV'

pmsh.mesher(geo_file, mesh_file, discretisation)
mesh = pmsh.read_mesh(mesh_file)


#%% VISUALISATION

x_plot = np.zeros(len(mesh))
plt.figure()
plt.plot([0, 4], [0, 0], 'r')     # physical domain
plt.plot(mesh, x_plot, 'o')         # centroids
plt.autoscale(enable=True, axis='x', tight=True)    # MATLAB's xlim tight
plt.show()