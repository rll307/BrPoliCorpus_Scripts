# -*- coding: utf-8 -*-

# =============================================================================
# Script name: 05_meta_csv.py
# Objective: Organise and leave only the metadata we need
# Variables to update:
#   1."folder_a =" Use the variable "output_folder" defined in 03_Build_Urls.py
#   2."folder_b =" provide the address in your system and the name this folder will have. The script will create it.
# =============================================================================

"""
Created on Tue Mar 26 22:40:08 2024
@author: Lima Lopes, Rodrigo Esteves de. Updating a previrous script by Yan, Ni
"""

import os
import re
# import shutil


def process_txt_files(input_folder, output_folder):
    # Loop through all subfolders and documents in folder A
    for root, dirs, files in os.walk(input_folder):
        for file_name in files:
            # Make sure the file is in txt format
            if file_name.endswith(".txt"):
                # Full path to build input file
                input_file_path = os.path.join(root, file_name)

                # Full path to build output file
                output_file_path = os.path.join(output_folder, file_name)

                # Read the document content line by line and process it
                with open(input_file_path, 'r', encoding='utf-8') as input_file:
                    lines = input_file.readlines()
                    extracted_content = ""
                    for line in lines:
                        # Use regular expressions to extract content
                        match = re.search(r'(Sessao|Quarto|Orador|Insercao|HorarioQuarto|sgFaseSessao|Data|Apelido|txFaseSessao|TipoSessao|HoraQuarto)=.*', line)
                        if match:
                            extracted_content += match.group(0) + "\n"

                    # Write the extracted content to the output file
                    with open(output_file_path, 'w', encoding='utf-8') as output_file:
                        output_file.write(extracted_content)

                print(f"Processing completed: {input_file_path}，and save to {output_file_path}")


# Specify the paths to folder A and folder B
folder_a = "URL_Fragment_L2"  # Change according to your system
folder_b = "meta"  # Change according to your system

# Create folder B
os.makedirs(folder_b, exist_ok=True)

# Process all txt documents in folder A and save the processing results to folder B
process_txt_files(folder_a, folder_b)

print("Document processing completed.")
