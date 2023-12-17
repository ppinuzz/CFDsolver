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




#test_read_mesh_1D()