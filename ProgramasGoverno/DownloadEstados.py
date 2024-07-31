import os
import requests
import pandas as pd
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import platform

# Detect the operating system and set Tesseract path
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

# List available CSV files
def list_csv_files():
    return [file for file in os.listdir() if file.endswith('.csv')]

# Download a file from a URL
def download_file(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {url} as {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

# Preprocess image for better OCR results
def preprocess_image(image):
    gray_image = image.convert('L')
    binary_image = gray_image.point(lambda x: 0 if x < 128 else 255, '1')
    return binary_image

# Extract text from a single PDF page
def extract_text_from_page(page):
    text = page.get_text()
    if text.strip():
        print(f"Copied text directly from page {page.number + 1}")
        return text
    else:
        print(f"Using OCR for page {page.number + 1}")
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes()))
        preprocessed_img = preprocess_image(img)
        return pytesseract.image_to_string(preprocessed_img, lang='por')  # Change 'por' to the correct language code

# Extract text from a PDF file
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

# Extract immediate folders for "year" and "Estado"
def extract_folders(path):
    parts = path.strip('/').split('/')
    if len(parts) >= 3:
        return parts[-3], parts[-1]
    else:
        return None, None

# Detect delimiter used in a CSV file
def detect_delimiter(file_path):
    with open(file_path, 'r') as f:
        first_line = f.readline()
        if ';' in first_line:
            return ';'
        elif ',' in first_line:
            return ','
        else:
            return None

# List CSV files in the current directory
csv_files = list_csv_files()
if not csv_files:
    print("No CSV files found in the current directory.")
    exit(1)

# Print the list of CSV files and ask the user to select one
print("Available CSV files:")
for idx, csv_file in enumerate(csv_files):
    print(f"{idx}: {csv_file}")

csv_idx = int(input("Enter the number of the CSV file to use: "))
selected_csv_file = csv_files[csv_idx]

if not os.path.exists(selected_csv_file):
    print(f"Error: '{selected_csv_file}' file not found.")
    exit(1)

# Extract "year" and "Estado" from the current directory
current_directory = os.getcwd()
year, estado = extract_folders(current_directory)
if not year or not estado:
    print("Error: Unable to extract 'year' and 'Estado' from the directory structure.")
    exit(1)

# Read URLs from urls.txt
try:
    with open('urls.txt', 'r') as url_file:
        urls = [line.strip() for line in url_file.readlines()]
except FileNotFoundError:
    print("Error: 'urls.txt' file not found.")
    exit(1)

# Detect delimiter in the selected CSV file
delimiter = detect_delimiter(selected_csv_file)
if delimiter is None:
    print("Error: Unable to detect the delimiter used in the CSV file.")
    exit(1)

# Read the CSV file with the detected delimiter
df = pd.read_csv(selected_csv_file, delimiter=delimiter)

# Add "year" and "Estado" columns to the DataFrame
df['year'] = year
df['Estado'] = estado

# Print the column names
print("Columns found in the selected CSV file:")
for idx, col in enumerate(df.columns):
    print(f"{idx}: {col}")

# Ask the user to choose the column containing the filenames
column_idx = int(input("Enter the number of the column containing the filenames: "))
column_name = df.columns[column_idx]

# Read filenames from the specified column and append ".pdf"
filenames = [filename.strip() + ".pdf" for filename in df[column_name].astype(str)]

# Check if both files have the same number of lines
if len(urls) != len(filenames):
    print("Error: The number of URLs and filenames do not match.")
    exit(1)

# Download each URL and save it with the corresponding filename
for url, filename in zip(urls, filenames):
    download_file(url, filename)

# Extract text from each downloaded PDF and save it in a new column
text_contents = []
for filename in filenames:
    print(f"Processing file: {filename}")
    text = extract_text_from_pdf(filename)
    text_contents.append(text)

df['text'] = text_contents

# Save the updated DataFrame back to a CSV file with the specified naming convention
output_csv_file = f"Governador_{estado}_{year}.csv"
df.to_csv(output_csv_file, index=False, sep=delimiter)
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
