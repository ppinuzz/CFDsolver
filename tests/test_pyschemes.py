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
from pycfd import pyschemes

# parent directory used for data files, w.r.t. to the MAIN project directory
parent_dir = 'tests/data/'
# directory used for junk data created by tests
junk_dir = 'tests/junk/'

def test_parse_terms():
    
    terms_exact = {'unsteady': True, 
             'convective': True, 
             'diffusive': True, 
             'source': False}
    
    terms_file = parent_dir + 'test.terms'
    terms_read = pyschemes.parse_terms(terms_file)
    
    success = (terms_exact == terms_read)
    
    assert success

