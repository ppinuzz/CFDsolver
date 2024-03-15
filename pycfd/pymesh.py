#!/usr/bin/env python3

import numpy as np
import os
import sys

def read_mesh(mesh_file):
    """
    Read 1D mesh from plain text file and import it

    Parameters
    ----------
    mesh_file : string
        Name of the mesh file

    Returns
    -------
    mesh : array
        1D mesh

    """
    
    # GET FILE CONTENT
    # read all lines at once and close the file 
    # (avoid corrupting mesh files)
    with open(mesh_file, 'r') as file:
        lines = file.readlines()
    
    # check that the files is not empty and does not contain only whitespaces
    check_empty_input(lines, "ERROR: Empty mesh file")
    
    
    # PARSE FILE CONTENT
    i = 0
    while i < len(lines):
        # remove eventual whitespaces (e.g. the trailing '\n' always present)
        line = lines[i].strip()
        
        # format of the file:
        #   KEYWORD
        #   VALUE
        # when you find a match for a keyword, this means that the NEXT line(s)
        # contain the numerical value.
        #if line == 'UNIT':
            # read content of the NEXT line (i.e. the one below the keyword)
            #unit = lines[i+1].strip()
            # and skip the next line by moving the counter 
            # (since you've already read the next line, move the "line pointer"
            # to the next line)
            #i = i + 1
        if line == 'COORDINATES':
            # all the lines below are numbers
            mesh_str = lines[i+1:]
            # stop the loop, since the COORDINATES keyword should be the last 
            # keyword in the file
            break
        
        # move "line pointer" to the next line
        i = i + 1

    
    # CONVERT COORDINATES INTO FLOATS
    mesh = []
    for line in mesh_str:
        # remove whitespace
        x_i = line.strip()
        x_i = float(x_i)
        mesh.append(x_i)
    mesh = np.array(mesh)
    
    return mesh


def print_mesh(mesh, mesh_file):
    """
    Print the mesh saving it in a plain text file

    Parameters
    ----------
    mesh : array
        Mesh coordinates
    mesh_file : string
        Name of the file where to save the mesh

    Returns
    -------
    None.

    """
    
    print('Saving mesh to \t\t\t' + os.path.abspath(mesh_file))
    with open(mesh_file, 'w') as file:
        file.write('COORDINATES\n')
        np.savetxt(file, mesh, newline='\n')


def read_input_geom(input_file):
    """
    Read geometry from input file

    Parameters
    ----------
    input_file : string
        Name of the input file required to generate the mesh

    Returns
    -------
    geometry : dictionary
        Parameters describing the geometry contained in the input file

    """

    print('Reading geometry from \t' + os.path.abspath(input_file))
    
    # GET FILE CONTENT
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # check that the files is not empty and does not contain only whitespaces
    check_empty_input(lines, "ERROR: Empty geometry input file")
    
    # PARSE FILE CONTENT
    i = 0
    while i < len(lines):
        # remove eventual whitespaces (e.g. the trailing '\n' always present)
        line = lines[i].strip()
        
        # format of the file:
        #   KEYWORD
        #   VALUE
        # when you find a match for a keyword, this means that the NEXT line(s)
        # contain the numerical value.
        if line == 'X0':
            # read content of the NEXT line (i.e. the one below the keyword)
            x0 = lines[i+1].strip()
            x0 = float(x0)
            # and skip the next line by moving the counter 
            # (since you've already read the next line, move the "line pointer"
            # to the next line)
            i = i + 1
        elif line == 'XL':
            xL = lines[i+1].strip()
            xL = float(xL)
            i = i + 1
        elif line == 'N':
            N = lines[i+1].strip()
            # the number of points is an INTEGER
            N = int(N)
            i = i + 1
        elif line == 'SPACING':
            spacing = lines[i+1].strip()
        
        # move "line pointer" to the next line
        i = i + 1
    
    geometry = {'x0': x0,
                'xL': xL,
                'N': N,
                'spacing': spacing}
    
    return geometry
    

def mesher(input_file, mesh_file, discr_method='cellcenter'):
    """
    Create a 1D mesh and save it to file

    Parameters
    ----------
    input_file : string
        Name of the input file required to generate the mesh
    mesh_file : string
        Mesh filename
    discr_method : string
        Type of discretisation used:
            
            - ``'cellcenter'`` : cell-center
            - ``'cellvertex'``: cell-vertex (NOT implemented) 

    Returns
    -------
    None.

    """
    
    geometry = read_input_geom(input_file)
    x0 = geometry['x0']
    xL = geometry['xL']
    N = geometry['N']
    spacing = geometry['spacing']
    
    
    # CREATE MESH
    if discr_method == 'cellcenter':
        # mesh spacing = width of a finite volume (if uniform spacing is used)
        dx = (xL - x0) / N
        # x0 is the boundary of the physical domain and the boundary of the 
        # first physical FV, but the centroid of the FV is dx/2 from its face
        xC_0 = x0 + dx/2
        xC_L = xL - dx/2
        # the centroids are equally spaced in the interval [xC_0, xC_L]
        mesh = np.linspace(xC_0, xC_L, N)
    
    
    # SAVE MESH TO FILE
    print_mesh(mesh, mesh_file)


def convert_raw_mesh(raw_mesh_file, mesh_file):
    """
    Convert raw coordinates into mesh format

    Parameters
    ----------
    raw_mesh_file : string
        Name of the file containing raw coordinates
    mesh_file : string
        Name of the converted mesh file

    Returns
    -------
    None.

    """
    
    # GET FILE CONTENT
    with open(raw_mesh_file, 'r') as file:
        # read without removing newlines \n
        lines = file.readlines()
    
    # check that the files is not empty and does not contain only whitespaces
    check_empty_input(lines, "ERROR: Empty mesh file")
    
    # CONVERSION
    with open(mesh_file, 'w') as file:
        file.write('COORDINATES\n')
        # since newlines are still there, simply concatenate all the elements
        # of the string into one (['0\n', '1\n'] becomes '0\n1\n')
        coord = ''.join(lines)
        # the single string thus obtained is already formatted as it should to
        # create the .mesh file
        file.write(coord)


def check_empty_input(lines_from_file, error_message):
    """
    Check if the lines read from a file are empty (or contain only whitespaces)
    and return the ``EOFError`` exception if that occurs

    Parameters
    ----------
    lines_from_file : list
        Text lines read from a file (with ``.readlines()`` usually)
    error_message : string
        Errore message to be associate with the ``EOFError`` exception

    Raises
    ------
    ``EOFError``
        In a way, if the file is empty or contains only whitespaces it is true
        that the file reader has reached EOF without encountering "anything 
        useful" for the solver/mesher

    Returns
    -------
    None.

    """
    
    # CHECK FOR EMPTY FILES
    # weirdly enough, [] == False and is the pythonic way to check if it's empty
    # (if 'lines' is empty, then 'not lines' == 'not []' == 'not False' = True)
    # https://stackoverflow.com/a/53522/17220538
    if not lines_from_file:
        raise EOFError(error_message)
    
    # CHECK FOR WHITESPACE-ONLY FILES
    # first glue together the entire file content to have a single string
    # (i.e. join without any separator, thus the '')
    all_lines = ''.join(lines_from_file)
    # then check if the obtaines string contains only whitespaces
    # https://stackoverflow.com/questions/2405292/
    if all_lines.isspace():
        raise EOFError(error_message)

