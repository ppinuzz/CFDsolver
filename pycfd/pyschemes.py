#!/usr/bin/env python3

import numpy as np
import os
from pycfd import pymesh

def parse_terms(terms_file):
    
    print('Reading terms from \t\t' + os.path.abspath(terms_file))
    with open(terms_file, 'r') as file:
        lines = file.readlines()

    # check that the files is not empty and does not contain only whitespaces
    pymesh.check_empty_input(lines, "ERROR: Empty terms file")
    
    # PARSE FILE CONTENT
    # remove the empty lines and those containing whitespaces (.strip() converts
    # them to '', which evaluates to False)
    # https://stackoverflow.com/a/3845449/17220538
    lines = [line_i for line_i in lines if line_i.strip()]
    terms = {'unsteady': None, 
             'convective': None, 
             'diffusive': None, 
             'source': None}
    
    i = 0
    while i < len(lines):
        # remove eventual whitespaces (e.g. the trailing '\n' always present)
        line = lines[i].strip()
        
        if line == 'UNSTEADY':
            # skip the current line and go to the next
            i = i + 1
            # the next line contains a string:
            #   True    that term is present
            #   False   that term is not present
            next_line = lines[i].strip()
            # turn it into a boolean using the return value of the string comparison
            terms['unsteady'] = (next_line.lower() == 'true')
        elif line == 'CONVECTIVE':
            i = i + 1
            next_line = lines[i].strip()
            terms['convective'] = (next_line.lower() == 'true')
        elif line == 'DIFFUSIVE':
            i = i + 1
            next_line = lines[i].strip()
            terms['diffusive'] = (next_line.lower() == 'true')
        elif line == 'SOURCE':
            i = i + 1
            next_line = lines[i].strip()
            terms['source'] = (next_line.lower() == 'true')
        
        # move to next line
        i = i + 1
        
    return terms


def parse_unsteady_scheme(schemes_file):
    
    print('Reading schemes from \t' + os.path.abspath(schemes_file))
    with open(schemes_file, 'r') as file:
        lines = file.readlines()

    # check that the files is not empty and does not contain only whitespaces
    pymesh.check_empty_input(lines, "ERROR: Empty terms file")
    
    
    # PARSE FILE CONTENT
    # remove the empty lines and those containing whitespaces (.strip() converts
    # them to '', which evaluates to False)
    # https://stackoverflow.com/a/3845449/17220538
    lines = [line_i for line_i in lines if line_i.strip()]
    unsteady = {}
    
    i = 0
    while i < len(lines):
        # remove eventual whitespaces (e.g. the trailing '\n' always present)
        line = lines[i].strip()
        
        if line == 'UNSTEADY':
            # skip the current line and go to the next
            i = i + 1
            next_line = lines[i].strip()
            # remove blank spaces
            next_line = next_line.replace(' ', '')
            # if the next line contains a new term,then you've gone too far
            # and there are no more info related to the unsteady term
            while next_line != 'CONVECTIVE' and next_line != 'DIFFUSIVE' and next_line != 'SOURCE':
                # the next line has syntax
                #   quantityName: schemeName
                next_line = next_line.split(':')
                quantity = next_line[0]
                scheme = next_line[1]
                unsteady[quantity] = scheme
                # move to next line
                i = i + 1
                next_line = lines[i].strip()
                next_line = next_line.replace(' ', '')
            return unsteady
        
        i = i + 1
    
    return unsteady
    
    