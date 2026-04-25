import PyPDF2
import re

def extract_book_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

    # Clean and preprocess
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    text = text.strip()
    return text