# HOW TO MAKE THE MODULE AVAILABLE TO ALL THE TESTS AND CODES
# (https://docs.python-guide.org/writing/structure/#test-suite)

import os
import sys

# retrieve the path of the directory ('scripts') where this file is
path_this_dir = os.path.dirname(__file__)
# append '..' to it, thus creating a path pointing to the parent directory of
# the 'scripts' directort
# (APPARENTLY, '/path/to/file/..' is equivalent to '/path/to' because the '..'
# is always interpreted as the parent directory)
path_parent_dir = os.path.join(path_this_dir, '..')
# convert the path to an absolute path (probably useless, but it's safer)
abs_path_parent_dir = os.path.abspath(path_parent_dir)
# insert the path in the 'sys.path' list, where Python looks for when importing
# modules
sys.path.insert(0, abs_path_parent_dir)

#import pycfd.pymesh as pymesh