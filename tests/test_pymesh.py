"""
Unit tests for the 1D mesher

To run all tests: navigate to the top-level directory and execute:
pytest

To run tests for just one file:
pytest file_to_test.py

"""

import numpy as np
from pymesh import pymesh

def test_read_mesh_1D():
    """Test: read 1D .mesh file"""
    
    mesh_file = 'tests/test.mesh'
    
    mesh_exact = np.array([0. , 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1. ])
    mesh_read = pymesh.read_mesh(mesh_file)
    
    success = np.array_equal(mesh_exact, mesh_read)
    
    assert success


def test_raw_mesh_conversion():
    """Test: convert raw mesh coordinates to .mesh input file"""
    
    raw_mesh_file = 'tests/test_raw_mesh.txt'
    converted_mesh_file = 'test_converted_mesh.mesh'
    
    pymesh.convert_raw_mesh(raw_mesh_file, converted_mesh_file)
    mesh_converted = pymesh.read_mesh(converted_mesh_file)
    
    mesh_exact = np.array([0. , 0.1, 0.2, 0.3, 0.4])
    
    success = np.array_equal(mesh_exact, mesh_converted)
    
    assert success


def test_print_mesh():
    """Test: print mesh to .mesh file"""
    
    mesh = np.array([0, 0.1, 0.2, 0.3])
    mesh_file = 'test_print_mesh.mesh'
    pymesh.print_mesh(mesh, mesh_file)
    with open(mesh_file, 'r') as file:
        mesh_read = file.readlines()
    
    mesh_exact = ['COORDINATES\n',
     '0.000000000000000000e+00\n',
     '1.000000000000000056e-01\n',
     '2.000000000000000111e-01\n',
     '2.999999999999999889e-01\n']
    
    success = mesh_exact == mesh_read
    
    assert success


def test_1D_FD_mesh():
    """Test: create 1D finite difference mesh"""
    
    # nodal coordinates
    mesh_exact = np.array([0, 0.25, 0.5, 0.75, 1])
    
    input_file = 'tests/test_FD_input.input'
    mesh_file = 'test_1D_FD_mesh.mesh'
    discr_method = 'FD'
    pymesh.mesher(input_file, mesh_file, discr_method)
    mesh_created = pymesh.read_mesh(mesh_file)
    
    success = np.array_equal(mesh_created, mesh_exact)
    
    assert success


def test_1D_FV_mesh():
    """Test: create 1D finite volume mesh"""
    
    # centroid coordinates
    mesh_exact = np.array([0.5, 1.5, 2.5, 3.5])
    
    input_file = 'tests/test_FV_input.input'
    mesh_file = 'test_1D_FV_mesh.mesh'
    discr_method = 'FV'
    pymesh.mesher(input_file, mesh_file, discr_method)
    mesh_created = pymesh.read_mesh(mesh_file)
    
    success = np.array_equal(mesh_created, mesh_exact)
    
    assert success


def test_read_geom():
    """Test: read geometry from .input file"""
    
    input_file = 'tests/test_FV_input.input'
    geometry = pymesh.read_input_geom(input_file)
    
    correct_geom = {'x0': 0, 'xL': 4, 'N': 4, 'spacing': 'uniform'}
    
    success = correct_geom == geometry
    
    assert success