#!/usr/bin/env python3

import pycfd 
import matplotlib.pyplot as plt
import numpy as np

#%% PROVA

sample_folder = '../samplerun/'
geo_file = sample_folder + '/geometry.input'
mesh_file = sample_folder + 'sample.mesh'
discretisation = 'FV'

pycfd.mesher(geo_file, mesh_file, discretisation)
mesh = pycfd.read_mesh(mesh_file)


#%% VISUALISATION

x_plot = np.zeros(len(mesh))
plt.figure()
plt.plot(mesh, x_plot, 'o')
plt.show()