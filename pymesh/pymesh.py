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
    
    import numpy as np
    
    # GET FILE CONTENT
    # read all lines at once and close the file 
    # (avoid corrupting mesh files)
    with open(mesh_file, 'r') as file:
        lines = file.readlines()
    
    
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
    
    import numpy as np
    
    with open(mesh_file, 'w') as file:
        file.write('COORDINATES\n')
        np.savetxt(file, mesh, newline='\n')


def mesher(input_file, mesh_file, discr_method):
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
            'FD' : finite differences
            'FV': finite volumes

    Returns
    -------
    None.

    """
    
    import numpy as np
    
    # GET FILE CONTENT
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
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
    
    # CREATE MESH
    if discr_method == 'FD':
        mesh = np.linspace(x0, xL, N)
    elif discr_method == 'FV':
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
    
    # CONVERSION
    with open(mesh_file, 'w') as file:
        file.write('COORDINATES\n')
        # since newlines are still there, simply concatenate all the elements
        # of the string into one (['0\n', '1\n'] becomes '0\n1\n')
        coord = ''.join(lines)
        # the single string thus obtained is already formatted as it should to
        # create the .mesh file
        file.write(coord)



#%% PROVA

if __name__ == "__main__":
    #mesh_file = 'prova.mesh'
    
    #raw_mesh_file = 'prova_raw_mesh.txt'
    
    #mesh = read_mesh(mesh_file)
    
    #convert_raw_mesh(raw_mesh_file, 'converted_mesh.mesh', 'meter')
    
    input_file = '../tests/test_FV_input.input'
    
    mesher(input_file, 'mesh_FD.mesh', 'FV')

