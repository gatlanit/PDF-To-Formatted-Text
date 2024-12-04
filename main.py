from pdf2image import convert_from_path
import pytesseract

# Extract text from an image-based PDF file
def extract_text_from_image_pdf(pdf_path):
    extracted_text = []
    images = convert_from_path(pdf_path, dpi=300)
    for page_number, image in enumerate(images, start=1):
        print(f"Processing page {page_number}...")
        text = pytesseract.image_to_string(image)
        extracted_text.append(text)
    return "\n".join(extracted_text)

# Main processing
pdf_path = 'Test.pdf'
raw_text = extract_text_from_image_pdf(pdf_path)

# Save the reformatted text to a file
with open('output.txt', 'w') as file:
    file.write(raw_text)