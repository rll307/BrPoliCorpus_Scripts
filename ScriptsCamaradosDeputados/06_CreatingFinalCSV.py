# -*- coding: utf-8 -*-

# =============================================================================
# Script name: 06_CreatingFinalCSV.py
# Objective: Organise and leave only the metadata we need
# Variables to update:
#   1."folder_a =" Use the variable "folder_b" defined in 05_meta_csv.py
#   2."folder_b =" Use the variable "output_folder" defined in 04_Scraping.py
#   3."output_csv" Create an output csv file. Please, see our spreadsheet for the correct name
# =============================================================================

"""
Created on Tue Mar 26 22:40:08 2024
@author: Lima Lopes, Rodrigo Esteves de. Updating a previrous script by Yan, Ni
"""

import os
import csv
import urllib.parse
import pandas as pd


def parse_metadata(metadata_str):
    # Parse metadata string into a dictionary
    metadata = {}
    fields = metadata_str.split('&')
    for field in fields:
        key, value = field.split('=', 1)
        metadata[key] = urllib.parse.unquote(value)
    return metadata


def extract_content(file_path):
    # Extract content from a file
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def process_files(folder_a, folder_b, output_csv):
    # Initialize data list
    data = []

    # Iterate through metadata files in folder A
    for filename in os.listdir(folder_a):
        if filename.endswith('.txt'):
            # Parse metadata
            metadata_file_path = os.path.join(folder_a, filename)
            with open(metadata_file_path, 'r', encoding='utf-8') as meta_file:
                metadata_str = meta_file.read().strip()
            metadata = parse_metadata(metadata_str)

            # Match metadata with content file in folder B
            content_file_path = os.path.join(folder_b, filename)
            if os.path.exists(content_file_path):
                content = extract_content(content_file_path)
            else:
                content = ''

            # Remove 'nuInsercao' and 'txEtapa' from metadata
            metadata.pop('nuInsercao', None)
            metadata.pop('txEtapa', None)

            # Add metadata and content to data list
            row = {
                'Sessao': metadata.get('Sessao', ''),
                'Quarto': metadata.get('nuQuarto', ''),
                'Orador': metadata.get('nuOrador', ''),
                'HorarioQuarto': metadata.get('dtHorarioQuarto', ''),
                'FaseSessaoSG': metadata.get('sgFaseSessao', ''),
                'Data': metadata.get('Data', ''),
                'FaseSessao': metadata.get('txFaseSessao', ''),
                'TipoSessaoTXT': metadata.get('txTipoSessao', ''),
                'HoraQuarto': metadata.get('dtHoraQuarto', ''),
                'Discurso': content,
                'Apelido': metadata.get('txApelido', '')
            }
            data.append(row)

    # Write data to CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Sessao', 'Quarto', 'Orador', 'HorarioQuarto', 'FaseSessaoSG', 'Data', 'FaseSessao', 'TipoSessaoTXT', 'HoraQuarto', 'Discurso', 'Apelido']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


# Specify folder A, folder B, and the output CSV file path
folder_a = "meta"  # Change according to your system
folder_b = "fetched"  # Change according to your system
output_csv = "049_data.csv"  # Change according to your system

# Process files and create CSV
process_files(folder_a, folder_b, output_csv)

print("CSV file saved.")
