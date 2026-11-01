# -*- coding: utf-8 -*-
"""
BC Data Cleaning Script

Created on Sun Sep 17 08:41:26 2023

@author: Anita Taylor


Shit to do
- negative long
- Clean out date string
- Multiple datasets to pivot
- No well tag - not active
- missing data 
- lithology data
"""

#libraries

import pandas as pd

# Specify the file path or name
file = 'EMSWR_Rus_044403.csv'

# Drop additional rows 
# Create an empty list to store the data chunks and read in size of 100000

chunk_iter = pd.read_csv(file, chunksize=100000)

cols_to_delete = ['col1', 'col2', 'col3', 'col4']

elements_to_delete4SI = ['Element1', 'Element2', 'Element3']

elements_to_delete4Metals = []

elements_to_delete4Orgo = []

chunks = []

# Figure Out Parameter types
# Create an empty set to store the unique parameter names
parameter_names = set()

# Iterate over each chunk
for chunk in chunk_iter:
    # Update the set with the unique parameter names from the chunk
    parameter_names.update(chunk['PARAMETER NAME'].unique())

# Print the unique parameter names
for name in parameter_names:
    print(name)

# Cleaning 
# Iterate over each chunk
for chunk in chunk_iter:
    # Drop the specified columns and append the chunk to the list
    chunks.append(chunk.drop(cols_to_delete, axis=1))
    
#***data = pd.concat(chunks)
#***print(data.head())


filtered_chunks = []

for chunk in chunks:
    # Filter out the rows with PARAMETER NAME in elements_to_delete and append to the list
    filtered_chunks.append(chunk[~chunk['PARAMETER NAME'].isin(elements_to_delete)])

# Concatenate all filtered chunks into one DataFrame
filtered_data = pd.concat(filtered_chunks)

# Print the first 5 rows of the filtered data
print(filtered_data.head())


#Pivot this 

# Create an empty DataFrame to store the pivoted data
data_pivoted = pd.DataFrame()

#Iterate over each chunk
for chunk in chunk_iter:
    # Pivot the chunk
    chunk_pivoted = chunk.pivot_table(index=['EMS ID', 'LONGITUDE (Decimal Degrees)', 'LATITUTE (Decimal Degrees)', 'START DATE'],
                                      columns='PARAMETER NAME', values='Results', aggfunc='first').reset_index()
    # Append the pivoted chunk to the data
    data_pivoted = pd.concat([data_pivoted, chunk_pivoted])
