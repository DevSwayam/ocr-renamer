import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
import re
import os

# Configure Tesseract path if needed (uncomment and update path for Windows)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Function to extract dates from text
def extract_date_from_text(text):
    # Regex to capture dates preceded by "दिनांक", "Date", or similar
    date_pattern = r"(?:दिनांक|Date|Dated)[^\d]*(\d{2}[./-]\d{2}[./-]\d{4})"
    match = re.search(date_pattern, text)
    if match:
        return match.group(1)  # Return the first matched date
    return None

# Function to extract text from a PDF using PyMuPDF
def extract_text_with_pymupdf(pdf_path):
    try:
        pdf_document = fitz.open(pdf_path)
        text = ""
        for page in pdf_document:
            text += page.get_text("text")
        pdf_document.close()
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF with PyMuPDF: {e}")
        return None

# Function to extract text using OCR
def extract_text_with_ocr(pdf_path):
    try:
        images = convert_from_path(pdf_path)
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image, lang="hin+eng")  # Use Hindi and English OCR
        return text.strip()
    except Exception as e:
        print(f"Error performing OCR: {e}")
        return None

# Function to process a PDF and extract the date
def extract_date_from_pdf(pdf_path):
    # Try PyMuPDF first
    text = extract_text_with_pymupdf(pdf_path)
    if text:
        date = extract_date_from_text(text)
        if date:
            return date

    # Fall back to OCR if no text was extracted
    print(f"Falling back to OCR for {pdf_path}")
    text = extract_text_with_ocr(pdf_path)
    if text:
        return extract_date_from_text(text)

    return None

# Function to rename the file based on extracted date
def rename_pdf(original_path, extracted_date):
    directory, original_name = os.path.split(original_path)
    name, ext = os.path.splitext(original_name)

    # Extract the prefix and suffix of the file name
    if '.' in name:
        prefix, suffix = name.split('.', 1)
    else:
        prefix, suffix = name, ""

    # Build the new filename
    if extracted_date:
        new_name = f"{prefix}.{extracted_date}-{suffix}{ext}"
        new_path = os.path.join(directory, new_name)
        
        # Rename the file
        os.rename(original_path, new_path)
        return new_path
    return None

# Main function to process all PDFs in a folder
def process_pdfs_in_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            print(f"Processing: {filename}")
            extracted_date = extract_date_from_pdf(pdf_path)
            if extracted_date:
                renamed_path = rename_pdf(pdf_path, extracted_date)
                print(f"Renamed to: {renamed_path}")
            else:
                print(f"No date found in: {filename}")

if __name__ == "__main__":
    # Prompt user for folder path
    folder_path = input("Enter the folder path containing PDFs: ").strip()
    process_pdfs_in_folder(folder_path)
