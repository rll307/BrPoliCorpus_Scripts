# -*- coding: utf-8 -*-

# =============================================================================
# Script name: 02_URLDataFragments.py
# Objective: Generate base URL pre fragments
# Variables to update:
#   1."input_folder =" Use the variable "folder_a" defined in 01_links.py
#   2."output_parent_folder =" provide the address in your system and the name this folder will have. The script will create it.
# =============================================================================
"""
Created on Tue Mar 26 22:40:08 2024
@author: Lima Lopes, Rodrigo Esteves de. Updating a previrous script by Yan, Ni
"""

import os
import requests
import re
import chardet  # Import chardet library


def process_url(url, output_folder):
    # Send HTTP request to obtain the source code of the web page
    response = requests.get(url)
    # Use chardet to detect web page encoding
    encoding = chardet.detect(response.content)['encoding']
    html_code = response.content.decode(encoding)  # Decode web content using the detected encoding

    # Regular expression matching pattern
    pattern = re.compile(r'(TextoHTML[^*]*?txEtapa=)')

    # Match all content
    matches = pattern.finditer(html_code)

    # Create a folder to store the output
    os.makedirs(output_folder, exist_ok=True)

    # Initialize the number of matches
    i = 0

    # Across the matching results and output them to different txt documents
    for i, match in enumerate(matches, start=1):
        # Extract matching content
        matched_content = match.group(1)

        # Use regular expressions to replace tabs with spaces
        cleaned_content = re.sub(r'\t', '', matched_content)

        # Build output file path
        output_file_path = os.path.join(output_folder, f"{os.path.basename(output_folder)}-{i}.txt")

        # Output matching content to txt file
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(cleaned_content)

    print(f"Handle URL {url}，matched to {i} content and output to {output_folder} folder")


# Specify input folder A and output folder
input_folder = "A"  # Change according your system
output_parent_folder = "URL_Fragment"  # Change according your system

# Across each txt document in folder A
for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        # Build the full path of the txt file
        txt_file_path = os.path.join(input_folder, filename)

        # Read the URL in the txt file
        with open(txt_file_path, 'r', encoding='utf-8') as file:
            url = file.readline().strip()  # Read the first line as the URL

        # Build output folder path
        output_folder = os.path.join(output_parent_folder, os.path.splitext(filename)[0])

        # Process the URL and save the result
        process_url(url, output_folder)
