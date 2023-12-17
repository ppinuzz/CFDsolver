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
    

#%% PROVA

mesh_file = 'prova.mesh'

mesh = read_mesh(mesh_file)