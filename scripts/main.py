#!/usr/bin/env python3

# add the path of the module to sys.path, otherwise Python won't find it...
# (https://docs.python-guide.org/writing/structure/#test-suite)
import context
# submodules are NOT imported by default, you have to import them explicitly
# (https://stackoverflow.com/a/8899345/17220538)
import pycfd.pymesh as pmsh
import pycfd.pyschemes as psch
import matplotlib.pyplot as plt
import numpy as np


#%% PROVA

sample_folder = '../samplerun/'
geo_file = sample_folder + '/geometry.input'
mesh_file = sample_folder + 'sample.mesh'
pmsh.mesher(geo_file, mesh_file)
mesh = pmsh.read_mesh(mesh_file)

terms_file = sample_folder + 'sample.terms'
terms = psch.parse_terms(terms_file)

schemes_file = sample_folder + 'sample.schemes'
unsteady = psch.parse_unsteady_scheme(schemes_file)


#%% VISUALISATION

pmsh.plot_mesh(mesh, print_legend=True)