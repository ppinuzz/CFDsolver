#!/usr/bin/env python3

"""
Unit tests for the 1D mesher

To run all tests: navigate to the top-level directory and execute:
pytest

To run tests for just one file:
pytest file_to_test.py

"""

import numpy as np
import pytest
from pycfd import pymesh

# parent directory used for data files, w.r.t. to the MAIN project directory
parent_dir = 'tests/data/'
# directory used for junk data created by tests
junk_dir = 'tests/junk/'



def test_read_mesh_1D():
    """Test: read 1D .mesh file"""
    
    mesh_exact = {'centroids': np.array([0, 0.2, 0.4, 0.6, 0.8, 1]),
            'face_nodes':np.array( [-0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1])
            }
    
    mesh_file = parent_dir + 'test.mesh'
    mesh_read = pymesh.read_mesh(mesh_file)
    
    success = ((np.array_equal(mesh_exact['centroids'], mesh_read['centroids'])) and 
        (np.array_equal(mesh_exact['face_nodes'], mesh_read['face_nodes'])))
    
    assert success


def test_print_mesh():
    """Test: print mesh to .mesh file"""
    
    mesh_exact = {'centroids': np.array([0, 0.2, 0.4, 0.6, 0.8, 1]),
            'face_nodes':np.array( [-0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1])
            }
    mesh_file = junk_dir + 'test_print_mesh.mesh'
    pymesh.print_mesh(mesh_exact, mesh_file)
    with open(mesh_file, 'r') as file:
        mesh_read = file.readlines()
    
    mesh_exact = ['CENTROID COORDINATES\n',
        '0.000000000000000000e+00\n',
        '2.000000000000000111e-01\n',
        '4.000000000000000222e-01\n',
        '5.999999999999999778e-01\n',
        '8.000000000000000444e-01\n',
        '1.000000000000000000e+00\n',
    	'\n',
        'FACE NODES COORDINATES\n',
        '-1.000000000000000056e-01\n',
        '1.000000000000000056e-01\n',
        '2.999999999999999889e-01\n',
        '5.000000000000000000e-01\n',
        '6.999999999999999556e-01\n',
        '9.000000000000000222e-01\n',
        '1.100000000000000089e+00\n',
]
    
    success = (mesh_exact == mesh_read)
    
    assert success


def test_1D_cell_center_mesh():
    """Test: create 1D finite volume mesh"""
    
    mesh_exact = {'centroids': np.array([0, 0.2, 0.4, 0.6, 0.8, 1]),
            'face_nodes':np.array( [-0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1])
            }
    
    input_file = parent_dir + 'test_FV_input.input'
    mesh_file = junk_dir + 'test_1D_FV_mesh.mesh'
    discr_method = 'cellcenter'
    pymesh.mesher(input_file, mesh_file, discr_method)
    mesh_created = pymesh.read_mesh(mesh_file)
    
    tol = 1e-10
    diff_centroids = np.abs(mesh_created['centroids'] - mesh_exact['centroids'])
    diff_faces = np.abs(mesh_created['face_nodes'] - mesh_exact['face_nodes'])
    
    success = (diff_centroids < tol).all() and (diff_faces < tol).all()
    
    assert success


def test_read_geom():
    """Test: read geometry from .input file"""
    
    input_file = parent_dir + 'test_FV_input.input'
    geometry = pymesh.read_input_geom(input_file)
    
    correct_geom = {'xf_0': -0.1, 'xf_N': 1.1, 'N_fv': 6, 'spacing': 'uniform', 'expansion_ratio': None}
    
    success = correct_geom == geometry
    
    assert success


def test_check_empty_file():
    """Test: check whether the content of a file is non-existent (empty file)"""
    
    input_file = parent_dir + 'test_empty.input'
    with open(input_file, 'r') as file:
        lines_from_file = file.readlines()
    error_message = "ERROR: Empty file"
    
    # https://stackoverflow.com/a/56569533/17220538
    with pytest.raises(EOFError, match=error_message):
        pymesh.check_empty_input(lines_from_file, error_message)


def test_check_whitespaces_file():
    """Test: check whether the content of a file is composed of whitespaces only"""
    
    input_file = parent_dir + 'test_whitespace.input'
    with open(input_file, 'r') as file:
        lines_from_file = file.readlines()
    error_message = "ERROR: Only whitespaces in the file"
    
    # https://stackoverflow.com/a/56569533/17220538
    with pytest.raises(EOFError, match=error_message):
        pymesh.check_empty_input(lines_from_file, error_message)



if __name__ == '__main__':
    # I don't know why, but 
    #   import .context     works with pytest, not when run as a script
    #   import context      works when run as a script, not with pytest
    # Since 'context' is not strictly necessary when running pytest, let's use
    # it only when the file is run in 'script mode'
    import context
    
    # if you're running the file as a script, the paths must be relative to 
    # THIS file (I guess?)
    parent_dir = './data/'     # parent directory used for data files
    junk_dir = './junk/'       # directory used for junk data created by tests
    
    test_read_mesh_1D()
    #test_raw_mesh_conversion()
    test_print_mesh()
    test_1D_cell_center_mesh()
    test_read_geom()
    test_check_empty_file()
    test_check_whitespaces_file()
