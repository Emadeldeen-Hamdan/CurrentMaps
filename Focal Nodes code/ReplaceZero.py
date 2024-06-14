#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 22:13:51 2024

@author: emadeldeen
"""

import re

uploaded_file_path = 'test2/20002000_Raster.txt'

# Read 
with open(uploaded_file_path, 'r') as file:
    lines = file.readlines()

# Process the lines to replace 0s with -9999
processed_lines = [" ".join(['-9999' if value == '0' else value for value in line.split()]) + '\n'
                   for line in lines]
#Output
processed_file_path = './processed_replace_zeros.txt'
with open(processed_file_path, 'w') as file:
    file.write("".join(processed_lines))
