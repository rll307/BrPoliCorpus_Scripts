# -*- coding: utf-8 -*-

# =============================================================================
# Script name: 04_Scraping.py
# Objective: Get the texts and save them to a files
# Variables to update:
#   1."input_folder =" Use the variable "output_folder" defined in 03_Build_Urls.py
#   2."output_folder =" provide the address in your system and the name this folder will have. The script will create it.
# =============================================================================

"""
Created on Tue Mar 26 22:40:08 2024
@author: Lima Lopes, Rodrigo Esteves de. Updating a previrous script by Yan, Ni
"""
import os
import requests
from bs4 import BeautifulSoup
import re


import chardet


def fetch_content(url):
    # Send HTTP request to obtain web page content
    response = requests.get(url)

    if response.status_code == 200:
        # Use chardet to detect the encoding method of the web page
        encoding = chardet.detect(response.content)['encoding']

        # If the encoding cannot be detected, use the default UTF-8 encoding
        if not encoding:
            encoding = 'utf-8'

        # Use BeautifulSoup to parse HTML content and specify the encoding method
        soup = BeautifulSoup(response.content, "html.parser", from_encoding=encoding)

        # Find all <p> tags
        paragraphs = soup.find_all("p")

        # Extract the text content in the <p> tag
        extracted_text = ""
        for paragraph in paragraphs:
            extracted_text += paragraph.get_text() + "\n\n"

        # Remove redundant meta elements
        cleaned_text = re.sub(r'<(span|font)[^>]*>(.*?)</\1>', '', extracted_text)

        return cleaned_text
    else:
        print(f"Failed to fetch the webpage: {url}")
        return None


def process_folder(input_folder, output_folder):
    # Across all txt documents in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            # Build the full path of the txt file
            txt_file_path = os.path.join(input_folder, filename)

            # Read the URL in the txt file
            with open(txt_file_path, 'r', encoding='utf-8') as file:
                url = file.readline().strip()  # Read the first line as the URL

            # Capture web content
            content = fetch_content(url)

            if content:
                # Build output file path
                output_file_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")

                # Save the captured content into a txt document
                with open(output_file_path, "w", encoding="utf-8") as output_file:
                    output_file.write(content)

                print(f"Fetching completed: {url}，and saved to {output_file_path}")
            else:
                print(f"Unable to crawl: {url}")


# Specify input folder and output folder
input_folder = "URL_Fragment_L2"  # change according your system
output_folder = "fetched"  # change according your sysmtem

# Create output folder
os.makedirs(output_folder, exist_ok=True)

# Process all txt documents in the input folder
process_folder(input_folder, output_folder)

print("All web pages are fetched.")
