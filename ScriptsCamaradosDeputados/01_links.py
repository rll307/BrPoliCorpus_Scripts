# -*- coding: utf-8 -*-

# =============================================================================
# Script name: 01_links.py
# Objective: Get the urls and validates them
# Variables to update:
#   1. "dtInicio" = beginning of the search (see in the spreadsheet)
#   2. "dtFim"  = end of the search (see in the spreadsheet)
#   3.  "for current_page in range(2, x)" = change the "X" for the total of pages in the search (see in the spreadsheet)
#   4. "folder_a" = provide the address in your system and the name this folder will have. The script will create it
#   5. "folder_b" =  provide the address in your system and the name this folder will have. The script will create it
# =============================================================================
"""
Created on Tue Mar 26 22:40:08 2024
@author: Lima Lopes, Rodrigo Esteves de. Updating a previrous script by Yan, Ni
"""

import os
import requests

# Base URL change dates of research accoring to year


def generate_url(current_page):
    base_url = "https://www.camara.leg.br/internet/sitaqweb/resultadoPesquisaDiscursos.asp?"
    params = {
        "txIndexacao": "",
        "CurrentPage": current_page,
        "BasePesq": "plenario",
        "txOrador": "",
        "txPartido": "",
        "dtInicio": "01/11/2006",  # change here
        "dtFim": "31/12/2006",  # change here
        "txUF": "",
        "txSessao": "",
        "listaTipoSessao": "",
        "listaTipoInterv": "",
        "inFalaPres": "",
        "listaTipoFala": "",
        "listaFaseSessao": "",
        "txAparteante": "",
        "listaEtapa": "",
        "CampoOrdenacao": "dtSessao",
        "TipoOrdenacao": "DESC",
        "PageSize": "50",
        "txTexto": "",
        "txSumario": ""
    }
    url = base_url + "&".join([f"{key}={value}" for key, value in params.items()])
    return url


def check_url_validity(url):
    try:
        response = requests.get(url)
        return response.status_code // 100 == 2
    except requests.RequestException:
        return False


def save_to_file(url, folder, filename):
    filepath = os.path.join(folder, f"{filename}.txt")
    with open(filepath, "w") as file:
        file.write(url)


def main():
    # Specify the path to the folder. These should change according to your directory structure
    folder_a = "A"  # change here
    folder_b = "B"  # change here

    # Create folders
    os.makedirs(folder_a, exist_ok=True)
    os.makedirs(folder_b, exist_ok=True)

    for current_page in range(2, 87):  # Generate URLS (check the number of total pages on the updated table attached)
        url = generate_url(current_page)
        is_valid = check_url_validity(url)

        if is_valid:
            save_to_file(url, folder_a, str(current_page))
            print("URL", str(current_page), "exists")
        else:
            save_to_file(url, folder_b, str(current_page))
            print(f"URL {url} does not exist")


if __name__ == "__main__":
    main()
