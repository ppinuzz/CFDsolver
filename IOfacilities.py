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
        if line == 'UNIT':
            # read content of the NEXT line (i.e. the one below the keyword)
            unit = lines[i+1].strip()
            # and skip the next line by moving the counter 
            # (since you've already read the next line, move the "line pointer"
            # to the next line)
            i = i + 1
        elif line == 'COORDINATES':
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



def convert_raw_mesh(raw_mesh_file, mesh_file, unit):
    """
    Convert raw coordinates into mesh format

    Parameters
    ----------
    raw_mesh_file : string
        Name of the file containing raw coordinates
    mesh_file : string
        Name of the converted mesh file
    unit : string
        Unit of measure (e.g. 'meter')

    Returns
    -------
    None.

    """
    
    with open(raw_mesh_file, 'r') as file:
        # read without removing newlines \n
        lines = file.readlines()
    
    with open(mesh_file, 'w') as file:
        file.write('UNIT\n')
        file.write(unit + '\n\n')
        file.write('COORDINATES\n')
        # since newlines are still there, simply concatenate all the elements
        # of the string into one (['0\n', '1\n'] becomes '0\n1\n')
        coord = ''.join(lines)
        # the single string thus obtained is already formatted as it should to
        # create the .mesh file
        file.write(coord)
    


#%% PROVA

mesh_file = 'prova.mesh'

raw_mesh_file = 'prova_raw_mesh.txt'

mesh = read_mesh(mesh_file)

convert_raw_mesh(raw_mesh_file, 'converted_mesh.mesh', 'meter')
