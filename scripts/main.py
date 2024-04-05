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

pmsh.mesher(geo_file, mesh_file)
mesh = pmsh.read_mesh(mesh_file)


#%% VISUALISATION

# N finite volumes => N centroids => N+1 face nodes
N_fv = len(mesh['centroids'])
x_plot_centroids = np.zeros(N_fv)
x_plot_face_nodes = np.zeros(N_fv+1)
plt.figure()
plt.plot([0, 4], [0, 0], 'r')     # physical domain
plt.plot(mesh['centroids'], x_plot_centroids, 'o', label='centroids $x_P$')
plt.plot(mesh['face_nodes'], x_plot_face_nodes, '*', label='face nodes $x_f$')
plt.autoscale(enable=True, axis='x', tight=True)    # MATLAB's xlim tight
plt.legend()
plt.show()