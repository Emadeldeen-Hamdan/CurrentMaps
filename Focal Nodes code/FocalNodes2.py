#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 22:04:39 2024

@author: emadeldeen
"""

import re

# Let's read the content of the uploaded text file to process it
uploaded_file_path = 'test2/20002000_Raster.txt'

# Read the content of the file
with open(uploaded_file_path, 'r') as file:
    lines = file.readlines()

# Process the lines
# Find the line containing the "NODATA_value"
nodata_line_index = next(i for i, line in enumerate(lines) if "NODATA_value" in line)
nodata_value = int(lines[nodata_line_index].split()[-1])  # Read as integer

# Replace all data values with NODATA_value starting from the line after "NODATA_value"
data_lines = lines[nodata_line_index + 1:]
processed_data_lines = [" ".join([str(nodata_value) if re.match(r'^-?\d+(\.\d+)?$', value) else value for value in line.split()]) + '\n'
                        for line in data_lines]

# Combine header and processed data
processed_content = "".join(lines[:nodata_line_index + 1]) + "".join(processed_data_lines)

# Write the processed content back to a new file
processed_file_path = './processed_focal.txt'
with open(processed_file_path, 'w') as file:
    file.write(processed_content)

# Read the content of the processed file
file_path = 'processed_focal.txt'
with open(file_path, 'r') as file:
    lines = file.readlines()

# Extract the header information
ncols = int(lines[0].split()[1])
nrows = int(lines[1].split()[1])
nodata_value = int(lines[6].split()[1])  # Ensure nodata_value is an integer

# Extract the grid data and convert to integer values
grid_data = [list(map(int, re.findall(r'-?\d+', line))) for line in lines[6:]]

# Let's re-define the fill_rectangle function to handle multiple fill operations
def fill_multiple_rectangles(grid, operations):
    """
    Fill multiple rectangle areas in the grid data with specified values.

    :param grid: List of lists representing the grid.
    :param operations: List of dictionaries, each containing the parameters for a fill operation.
    :return: None, modifies the grid in-place.
    """
    for operation in operations:
        start_row = operation['start_row'] - 1  # Convert to 0-indexed
        end_row = operation['end_row'] - 1
        start_col = operation['start_col'] - 1
        end_col = operation['end_col'] - 1
        fill_value = operation['fill_value']

        # Fill the specified rectangle with the fill_value
        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                if 0 <= r < nrows and 0 <= c < ncols:  # Check within grid bounds
                    grid[r][c] = fill_value

# Define the operations
operations = [
    {'start_row': 720, 'end_row': 724, 'start_col': 568, 'end_col': 572, 'fill_value': 1},
    {'start_row': 844, 'end_row': 848, 'start_col': 896, 'end_col': 900, 'fill_value': 2},
    {'start_row': 1053, 'end_row': 1057, 'start_col': 900, 'end_col': 904, 'fill_value': 3},
    {'start_row': 1209, 'end_row': 1213, 'start_col': 661, 'end_col': 665, 'fill_value': 4}
    #You can add more
]

# Apply the fill operations on the grid data
fill_multiple_rectangles(grid_data, operations)

# Combine header and modified grid data back into a single string
processed_lines = [' '.join(map(str, row)) + '\n' for row in grid_data]
processed_content = ''.join(lines[:6]) + ''.join(processed_lines)

# Write the processed content to a new file
output_file_path = './test3/20002000_focalnodes.txt'
with open(output_file_path, 'w') as file:
    file.write(processed_content)
