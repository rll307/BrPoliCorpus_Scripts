import os
import requests
import pandas as pd
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import platform

# Detect the operating system
def set_tesseract_path():
    system = platform.system()
    if system == 'Windows':
        return r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust path as needed
    elif system == 'Linux':
        return r'/usr/bin/tesseract'
    elif system == 'Darwin':  # macOS
        return r'/usr/local/bin/tesseract'
    else:
        raise OSError('Unsupported operating system')

pytesseract.pytesseract.tesseract_cmd = set_tesseract_path()

def list_csv_files():
    return [file for file in os.listdir() if file.endswith('.csv')]

def download_file(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {url} as {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

def preprocess_image(image):
    gray_image = image.convert('L')
    binary_image = gray_image.point(lambda x: 0 if x < 128 else 255, '1')
    return binary_image

def extract_text_from_page(page):
    text = page.get_text()
    if text.strip():
        return text
    else:
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes()))
        preprocessed_img = preprocess_image(img)
        return pytesseract.image_to_string(preprocessed_img, lang='por')  # Change 'por' to the correct language code

def extract_text_from_pdf(filename):
    text = ""
    try:
        doc = fitz.open(filename)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += extract_text_from_page(page)
        doc.close()
    except Exception as e:
        print(f"Failed to extract text from {filename}: {e}")
    return text

def extract_ano(path):
    parts = path.strip('/').split('/')
    if len(parts) >= 2:
        return parts[-2]
    else:
        return None

# List CSV files in the current directory
csv_files = list_csv_files()
print("Available CSV files:")
for idx, csv_file in enumerate(csv_files):
    print(f"{idx}: {csv_file}")

# Prompt user to select a CSV file
csv_idx = int(input("Enter the number of the CSV file to use: "))
selected_csv_file = csv_files[csv_idx]

if not os.path.exists(selected_csv_file):
    print(f"Error: '{selected_csv_file}' file not found.")
    exit(1)

# Extract the year from one level up the directory structure
current_directory = os.getcwd()
ano = extract_ano(current_directory)
if not ano:
    print("Error: Unable to extract 'Ano' from the directory structure.")
    exit(1)

# Read URLs from urls.txt
try:
    with open('urls.txt', 'r') as url_file:
        urls = [line.strip() for line in url_file.readlines()]
except FileNotFoundError:
    print("Error: 'urls.txt' file not found.")
    exit(1)

# Read the selected CSV file
df = pd.read_csv(selected_csv_file, delimiter=';')

# Add a column for the year
df['year'] = ano

# Print the columns in the CSV file and prompt user to select the column containing filenames
print("Columns found in the selected CSV file:")
for idx, col in enumerate(df.columns):
    print(f"{idx}: {col}")

column_idx = int(input("Enter the number of the column containing the filenames: "))
column_name = df.columns[column_idx]

# Append ".pdf" to filenames
filenames = [filename.strip() + ".pdf" for filename in df[column_name].astype(str)]

# Check if the number of URLs matches the number of filenames
if len(urls) != len(filenames):
    print("Error: The number of URLs and filenames do not match.")
    exit(1)

# Download each file and save with the corresponding filename
for url, filename in zip(urls, filenames):
    download_file(url, filename)

# Extract text from each downloaded PDF and save in a new column
text_contents = []
for idx, filename in enumerate(filenames):
    print(f"Processing file {idx + 1}/{len(filenames)}: {filename}")
    text = extract_text_from_pdf(filename)
    text_contents.append(text)

df['text'] = text_contents

# Save the updated DataFrame to a new CSV file with the year in the filename
output_csv_file = f"Brasil_president_{ano}.csv"
df.to_csv(output_csv_file, index=False, sep=';')
print(f"Updated DataFrame saved to {output_csv_file}")

# Delete the source CSV file
try:
    os.remove(selected_csv_file)
    print(f"Deleted source CSV file: {selected_csv_file}")
except OSError as e:
    print(f"Error: {e.strerror} - {selected_csv_file}")

# Delete the downloaded PDF files
for filename in filenames:
    try:
        os.remove(filename)
        print(f"Deleted PDF file: {filename}")
    except OSError as e:
        print(f"Error: {e.strerror} - {filename}")
