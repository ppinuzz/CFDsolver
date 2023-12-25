#!/bin/python3

import argparse
#from pycfd import pymesh

# CREATE PARSER
mesh_parser = argparse.ArgumentParser(
            prog="pymesh",
            description="Create 1D finite difference or finite volume meshes",
            # force the user to enter the EXACT flags, not abbreviated versions
            allow_abbrev=False)

# ADD ARGUMENTS (positional and optional)
# required=True     forces them to be mandatory even it the "--syntax" is the 
#                   one used for optional arguments
#mesh_parser.add_argument("-g", "--geo-file", action="store", required=True)
#mesh_parser.add_argument("-m", "--mesh-file", action="store", required=True)
# (by default, input values are STRINGS!)
#mesh_parser.add_argument("-d", "--discretisation", action="store", type=int, required=True)
mesh_parser.add_argument("geo_file",)
mesh_parser.add_argument("mesh_file")
# (by default, input values are STRINGS!)
mesh_parser.add_argument("discretisation", type=int)
# version number
mesh_parser.add_argument("-v", "--version", 
                        action="version", 
                        version="%(prog)s 0.0.0")

# PARSE THE ARGUMENTS passed to the script
args = mesh_parser.parse_args()

# USE ARGUMENTS
#pymesh.mesher(args.geo_file, args.mesh_file, args.discretisation)
