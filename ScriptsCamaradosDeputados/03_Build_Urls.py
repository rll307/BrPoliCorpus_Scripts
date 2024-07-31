# -*- coding: utf-8 -*-

# =============================================================================
# Script name: 03_Build_Urls.py
# Objective: Build the URLs based on metadata
# Variables to update:
#   1."input_folder =" Use the variable "output_parent_folder" defined in 02_URLDataFragments.py
#   2."output_folder =" provide the address in your system and the name this folder will have. The script will create it.
# =============================================================================
"""
Created on Tue Mar 26 22:40:08 2024
@author: Lima Lopes, Rodrigo Esteves de. Updating a previrous script by Yan, Ni
"""
import os
from urllib.parse import quote

# Specify input folder and output folder
input_folder = "URL_Fragment"  # change according your system
output_folder = "URL_Fragment_L2"  # change according your system

# Create output folder
os.makedirs(output_folder, exist_ok=True)


def parse_txt_to_dict(txt_file_path):
    # Read the content in the txt file and parse it into a dictionary
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file.readlines()]

# Delete the first line
    lines.pop(0)
    # 解析为字典
    result_dict = {}
    for line in lines:
        if "=" in line:
            key, value = line.split("=")
            key = key.replace("&amp;", "")
            value = quote(value)
            result_dict[key] = value

    return result_dict


# Across one level of folders
for folder in os.listdir(input_folder):
    print(folder)
    subfolder_path = os.path.join(input_folder, folder)

    # Determine whether it is a folder
    if os.path.isdir(subfolder_path):
        # Across each txt document
        for filename in os.listdir(subfolder_path):
            if filename.endswith(".txt"):

                txt_file_path = os.path.join(subfolder_path, filename)

                print(subfolder_path)

                # Parse txt document into dictionary
                parameters_dict = parse_txt_to_dict(txt_file_path)

                # Merge URLS
                base_url = "https://www.camara.leg.br/internet/sitaqweb/"

                url_beginn = "TextoHTML.asp?etapa=5&"

                url_parameters = "&".join([f"{key}={value}" for key, value in parameters_dict.items()])

                full_url = base_url + url_beginn + url_parameters
                # Build output file path
                output_file_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_result.txt")

                # Output the URL to the result file
                with open(output_file_path, "w", encoding="utf-8") as output_file:
                    output_file.write(full_url)

print(f"Processing is completed and the results are saved to {output_folder} folder.")
