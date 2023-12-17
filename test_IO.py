# TESTS FOR IO FUNCTIONS (MESH-RELATED, FOR NOW)

import numpy as np
import IOfacilities as io

def test_read_mesh_1D():
    """Test to read 1D .mesh file"""
    
    mesh_file = 'prova.mesh'
    
    mesh_exact = np.array([0. , 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1. ])
    mesh_read = io.read_mesh(mesh_file)
    
    success = np.array_equal(mesh_exact, mesh_read)
    
    assert success


def test_raw_mesh_conversion():
    """Test to convert raw mesh coordinates to .mesh input file"""
    
    raw_mesh_file = 'prova_raw_mesh.txt'
    
    io.convert_raw_mesh(raw_mesh_file, 'converted_mesh_test.mesh', 'meter')
    mesh_converted = io.read_mesh('converted_mesh_test.mesh')
    
    mesh_exact = np.array([0. , 0.1, 0.2, 0.3, 0.4])
    
    success = np.array_equal(mesh_exact, mesh_converted)
    
    assert success
    


#test_read_mesh_1D()