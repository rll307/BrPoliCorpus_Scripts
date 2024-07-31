# -*- coding: utf-8 -*-

# =============================================================================
# Script name: 07_SplitColumns.py
# Objective: Organise and leave only the metadata we need
# Variables to update:
#   1."df = pd.read_csv("Data01.csv")" = change the csv file name to hat you just created
#   2."df.to_csv("Data01.csv", index=False) = change the csv file name to hat you just created. th idea is overwrite it.
# =============================================================================

"""
Created on Tue Mar 26 22:40:08 2024
@author: Lima Lopes, Rodrigo Esteves de.
"""

import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv("025_data.csv")

# Split the column 'ColumnName' based on a delimiter and expand it into two columns
split_df = df['Apelido'].str.split(',', 1, expand=True)

# Assign the new columns to the DataFrame
df['Nome'] = split_df[0]
df['Partido'] = split_df[1]

# Drop the original column
df.drop(columns=['Apelido'], inplace=True)
df.rename(columns={'Nome': 'Apelido'}, inplace=True)

split_df = df['Partido'].str.split('-', 1, expand=True)

# Assign the new columns to the DataFrame
df['Estado'] = split_df[0]
df['P'] = split_df[1]

# Drop the original column
df.drop(columns=['Partido'], inplace=True)
df.rename(columns={'P': 'Partido'}, inplace=True)

# Save the modified DataFrame back to CSV
df.to_csv("025_data.csv", index=False)
