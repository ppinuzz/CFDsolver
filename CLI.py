#!/bin/python3

import argparse
from pycfd import pymesh

# create parser
mesh_parser = argparse.ArgumentParser(
            prog="pymesh",
            description="Create 1D finite difference or finite volume meshes")

# add arguments (positional and optional)
mesh_parser.add_argument("geo_file")
#mesh_parser.add_argument("-g", "--geometry", action=)
mesh_parser.add_argument("mesh_file")
#mesh_parser.add_argument("-m", "--mesh", action=)
mesh_parser.add_argument("discretisation")

# parse the arguments passed to the script
args = mesh_parser.parse_args()

# and use them as you please
pymesh.mesher(args.geo_file, args.mesh_file, args.discretisation)
