#!/usr/bin/env python3

import numpy as np
import os



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
        Parameters describing the geometry contained in the input file:
            
            - ``'xf_0'``: first face node, corresponding to point :math:`x_\mathrm{f} = a`
            - ``'xf_N'``: last face node, corresponding to point :math:`x_\mathrm{f} = b`
            - ``'N_fv'``: number :math:`N` of finite volumes (i.e. intervals) in :math:`[a,b]`
            - ``'spacing'``: type of spacing used. Current options:
                
                - ``'uniform'``: uniform spacing :math:`h = (b-a)/N`
                - ``'geometric'``: spacing follows a geometric series described by :math:`N` and the expansion ratio
            
            - ``'expansion_ratio'``: ratio of one element length to the next previous element lenght :math:`h_i/h_{i-1}`. Set to ``None`` if a ``'uniform'`` spacing is read, otherwise should be > 1.
    
    """

    print('Reading geometry from \t' + os.path.abspath(input_file))
    
    # GET FILE CONTENT
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # check that the files is not empty and does not contain only whitespaces
    check_empty_input(lines, "ERROR: Empty geometry input file")
    
    # PARSE FILE CONTENT
    i = 0
    # set initially to None, so that the code won't break if no expansion ratio
    # is given by the user (not needed for uniform spacing)
    exp_ratio = None
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
            spacing = spacing.lower()
            i = i + 1
        elif line == 'EXPANSION_RATIO':
            # read the line only if the spacing is non-uniform
            # (there's no expansion rate with uniform spacing)
            if spacing != 'uniform':
                exp_ratio = lines[i+1].strip()
                exp_ratio = float(exp_ratio)
            i = i + 1
        
        # move "line pointer" to the next line
        i = i + 1
    
    geometry = {'xf_0': x0,
                'xf_N': xL,
                'N_fv': N,
                'spacing': spacing,
                'expansion_ratio': exp_ratio
                }
    
    return geometry



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
    xf_0 = geometry['x0']
    xf_N = geometry['xL']
    N_fv = geometry['N']
    spacing = geometry['spacing']
    exp_ratio = geometry['expansion_ratio']
    
    
    # CREATE MESH
    if discr_method == 'cellcenter':
        if spacing == 'uniform':
            # mesh spacing = width of a finite volume (if uniform spacing is used)
            dx = (xf_N - xf_0) / N_fv
            # xf_0 is the boundary of the physical domain and the boundary of the 
            # first physical FV, but the centroid of the FV is dx/2 from its face
            xC_0 = xf_0 + dx/2
            xC_N = xf_N - dx/2
            # the centroids are equally spaced in the interval [xC_0, xC_N]
            xC = np.linspace(xC_0, xC_N, N_fv)
            # face nodes
            xf = np.linspace(xf_0, xf_N, N_fv+1)    # N volumes => N+1 face nodes
            
        elif spacing == 'geometric':
            # length of the 1st cell (smallest if exp_ratio > 1, largest if < 1)
            # sum of the terms alpha^(i-1) for i=1,...,N (geometric series)
            sum_geom_series = (1 - exp_ratio**N_fv) / (1 - exp_ratio)
            h_1 = (xf_N - xf_0) / sum_geom_series
            # centroids
            xC = np.zeros(N_fv)
            # face nodes
            xf = np.zeros(N_fv+1)  # N intervals => N+1 face nodes
            xf[0] = xf_0
            xf[-1] = xf_N
            i = 1
            while i < N_fv:
                h_i = h_1 * exp_ratio**(i-1)
                xf[i] = xf[i-1] + h_i
                xC[i-1] = (xf[i] + xf[i-1]) / 2     # midpoint of the interval
                i = i + 1
        
        mesh = {'centroids': xC,
                'face_nodes': xf
                }
    
    # SAVE MESH TO FILE
    print_mesh(mesh, mesh_file)



def calculate_expansion_ratio(N, xf_0, xf_N, h_1, alpha_0=1.05, tol=1e-8, k_max=200):
    
    # coefficient of the equation (compute once to avoid overhead)
    K = (xf_N - xf_0) / h_1
    # fixed point iteration function (fun(alpha) = alpha)
    fun = lambda alpha: alpha**N + (1-K)*alpha + K - 1
    
    k = 0
    err = tol + 1
    alpha_old = alpha_0
    while k < k_max and err > tol:
        alpha_new = fun(alpha_old)
        err = abs(alpha_new - alpha_old) / abs(alpha_old)
        alpha_old = alpha_new
        k = k + 1
    
    # set the flag to True to notify the user that the maximum number of
    # iterations have been exceed
    if k == k_max:
        max_iteration_reached = True
    else:
        max_iteration_reached = False
    
    return alpha_new, err, k, max_iteration_reached



def print_mesh(mesh, mesh_file):
    """
    Print the mesh saving it in a plain text file

    Parameters
    ----------
    mesh : dictionary
        Mesh coordinates:
            
            - ``'centroids'``: centroid coordinates :math:`x_P`
            - ``'face_nodes'``: face centre coordinates :math:`x_\mathrm{f}`
    mesh_file : string
        Name of the file where to save the mesh

    Returns
    -------
    None.

    """
    
    print('Saving mesh to \t\t\t' + os.path.abspath(mesh_file))
    with open(mesh_file, 'w') as file:
        file.write('COORDINATES\n')
        np.savetxt(file, mesh['centroids'], newline='\n')



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


