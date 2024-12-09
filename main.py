from pdf2image import convert_from_path
import pytesseract
import re
from concurrent.futures import ThreadPoolExecutor

# Precompiled regex patterns
patterns = [
    (re.compile(r"^.*?JUDGE:\s*", flags=re.DOTALL), ""),  # Remove JUDGE:
    (re.compile(r"Case.*?Page \d+ of \d+\n"), ""), # Remove page number
    (re.compile(r"^\d+\s*$", flags=re.MULTILINE), ""), # Remove standalone numbers
    (re.compile(r"\n{2,}"), "\n"), # Remove mutliple new lines
    (re.compile(r"[ \t]{2,}"), " "), # Remove multiple spaces
    (re.compile(r'\([^)]*\)'), '') # Remove parentehsis and its contents
]

def clean_text(text):
    # Remove Hearing closed
    text = re.sub(r"\(\s*The\s+Hearing\s+closed\s+at.*$", "", text, flags=re.DOTALL | re.IGNORECASE)
    
    for pattern, replacement in patterns:
        text = pattern.sub(replacement, text)
    return text.strip()  # Remove leading/trailing whitespace


def reformat_text(text):
    lines = text.split('\n')
    reformatted = []
    current_line = ""
    for line in lines:
        if re.match(r"^[A-Z]+:", line):
            if current_line:
                reformatted.append(current_line.strip())
            current_line = f"{line.strip()}"
        else:
            current_line += f" {line.strip()}"
    if current_line:
        reformatted.append(current_line.strip())
    return '\n'.join(reformatted)

def ocr_image(image):
    return pytesseract.image_to_string(image, config="--psm 6 --oem 3")

def extract_text_from_image_pdf(pdf_path):
    images = convert_from_path(pdf_path, dpi=150, thread_count=4)
    with ThreadPoolExecutor() as executor:
        extracted_text = list(executor.map(ocr_image, images))
    return "\n".join(extracted_text)

pdf_path = 'Test.pdf'
raw_text = extract_text_from_image_pdf(pdf_path)
formatted_text = clean_text(raw_text)
final_output = reformat_text(formatted_text)

with open('output.txt', 'w') as file:
    file.write(final_output)
