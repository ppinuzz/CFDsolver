# TESTS FOR MESH FUNCTIONS

import numpy as np
import pymesh as pmsh

def test_read_mesh_1D():
    """Test: read 1D .mesh file"""
    
    mesh_file = 'test.mesh'
    
    mesh_exact = np.array([0. , 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1. ])
    mesh_read = pmsh.read_mesh(mesh_file)
    
    success = np.array_equal(mesh_exact, mesh_read)
    
    assert success


def test_raw_mesh_conversion():
    """Test: convert raw mesh coordinates to .mesh input file"""
    
    raw_mesh_file = 'test_raw_mesh.txt'
    converted_mesh_file = 'test_converted_mesh.mesh'
    
    pmsh.convert_raw_mesh(raw_mesh_file, converted_mesh_file)
    mesh_converted = pmsh.read_mesh(converted_mesh_file)
    
    mesh_exact = np.array([0. , 0.1, 0.2, 0.3, 0.4])
    
    success = np.array_equal(mesh_exact, mesh_converted)
    
    assert success


def test_print_mesh():
    """Test: print mesh to .mesh file"""
    
    mesh = np.array([0, 0.1, 0.2, 0.3])
    mesh_file = 'test_read_mesh.mesh'
    pmsh.print_mesh(mesh, mesh_file)
    
    mesh_read = pmsh.read_mesh(mesh_file)
    
    success = np.array_equal(mesh, mesh_read)
    
    assert success
    