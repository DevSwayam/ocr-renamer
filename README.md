
# PDF Date Extractor and Renamer

## Overview

This script processes PDF files in a specified folder, extracts dates from their contents (both text-based and image-based), and renames the files to include the extracted date in the format:

`<original_prefix>.<extracted_date>-<original_suffix>.pdf`

The script supports multilingual text (e.g., Hindi and English) and can handle both text-based PDFs and scanned/image-based PDFs by leveraging **OCR (Optical Character Recognition)**.

---

## Features

- **Date Extraction**: Automatically detects dates in formats like `DD/MM/YYYY`, `DD-MM-YYYY`, and `DD.MM.YYYY`, preceded by keywords such as "दिनांक", "Date", or "Dated".
- **Text and Image Support**:
  - Extracts text from PDFs using PyMuPDF (`fitz`).
  - Falls back to OCR using `pytesseract` and `pdf2image` for scanned PDFs.
- **Automated Renaming**: Renames the PDF files based on the extracted date while preserving other filename components.

---

## Prerequisites

### Python Libraries
Install the required libraries using pip:
```bash
pip install pymupdf pytesseract pdf2image
```

### Tesseract OCR
#### macOS:
```bash
brew install tesseract
```

#### Linux:
```bash
sudo apt install tesseract-ocr
```

#### Windows:
1. Download Tesseract from [here](https://github.com/tesseract-ocr/tesseract).
2. Add its installation directory (e.g., `C:\Program Files\Tesseract-OCR`) to your system's PATH.

### Poppler
`pdf2image` requires Poppler for PDF-to-image conversion.

#### macOS:
```bash
brew install poppler
```

#### Linux:
```bash
sudo apt install poppler-utils
```

#### Windows:
1. Download Poppler from [here](http://blog.alivate.com.au/poppler-windows/).
2. Add the `bin` folder from the extracted directory to your system's PATH.

---

## Usage

1. **Prepare Your Folder**:
   - Place all the PDFs you want to process in a folder (e.g., `./pdfs`).

2. **Run the Script**:
   ```bash
   python3 script_name.py
   ```

3. **Input the Folder Path**:
   - When prompted, provide the folder path containing the PDFs. For example:
     ```
     Enter the folder path containing PDFs: ./pdfs
     ```

4. **Output**:
   - PDFs will be renamed to include the extracted date. Example:
     - Original: `report.summary.pdf`
     - Renamed: `report.04-01-2021-summary.pdf`

---

## Example

### Input File:
**Filename**: `145. PMI Electro.pdf`  
**Content**:
```
दिनांक 04/01/2021: Important meeting details.
```

### Output:
**Renamed File**: `145.04-01-2021-PMI Electro.pdf`

---

## How It Works

1. **Extracting Dates**:
   - The script first tries to extract text using PyMuPDF (`fitz`).
   - If no text is found or the PDF contains images, it uses OCR (`pytesseract`) to extract text.

2. **Regex Matching**:
   - The script identifies dates using regex patterns:
     ```regex
     (?:दिनांक|Date|Dated)[^\d]*(\d{2}[./-]\d{2}[./-]\d{4})
     ```

3. **Renaming**:
   - The script preserves the original filename structure (`<prefix>.<suffix>.pdf`) and appends the extracted date.

4. **Fallbacks**:
   - If no date is found, the file remains unchanged.

---

## Troubleshooting

### Common Errors

1. **`Error performing OCR: Unable to get page count. Is poppler installed and in PATH?`**
   - Ensure Poppler is installed and added to your system's PATH.

2. **`Error: Tesseract not found`**
   - Install Tesseract and ensure its binary is accessible via PATH.

3. **`No date found in PDF`**
   - Verify that the PDF contains readable text or dates matching the supported formats.

---

## Dependencies

- `fitz` (PyMuPDF): For extracting text from text-based PDFs.
- `pytesseract`: For OCR on image-based PDFs.
- `pdf2image`: For converting PDF pages to images for OCR.
- `Poppler`: Required by `pdf2image` for PDF processing.

---

## Limitations

- The script assumes dates follow formats like `DD/MM/YYYY` or `DD-MM-YYYY` and are preceded by "दिनांक", "Date", or "Dated".
- PDFs with complex layouts or non-standard formats might require manual handling.
