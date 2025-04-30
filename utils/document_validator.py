import cv2
import numpy as np
import pytesseract
from PIL import Image
import io
import re

def process_image_ocr(uploaded_file):
    """
    Process an uploaded image file with OCR to extract text.
    
    Args:
        uploaded_file: The uploaded file from Streamlit file_uploader
        
    Returns:
        str: Extracted text from the image
    """
    # Read the image file
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold to get image with only black and white
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    # Convert the processed image back to PIL Image for tesseract
    pil_img = Image.fromarray(thresh)
    
    # Extract text using tesseract
    try:
        text = pytesseract.image_to_string(pil_img, lang='por+eng')
        return text
    except Exception as e:
        print(f"Error in OCR processing: {e}")
        return ""

def validate_document(extracted_text, personal_info):
    """
    Validate the extracted text from a document against the user's personal information.
    
    Args:
        extracted_text (str): Text extracted from the document image
        personal_info (dict): User's personal information
        
    Returns:
        tuple: (is_valid, message) - Whether the document is valid and a validation message
    """
    # This is a simplified validation - in a real implementation, 
    # you would use more sophisticated methods and actual ID verification
    
    if not extracted_text:
        return False, "Could not extract text from the document. Please upload a clearer image."
    
    # Check if the name from personal info appears in the document
    name = personal_info.get('name', '').strip().lower()
    if name and len(name) > 3:  # Make sure we have a valid name to check
        if name in extracted_text.lower():
            # Attempt to find CPF in the extracted text
            cpf = personal_info.get('cpf', '').strip()
            if cpf:
                # Remove any formatting from CPF for comparison
                cpf_clean = re.sub(r'[^\d]', '', cpf)
                
                # Look for CPF pattern in the text
                cpf_pattern = r'\d{3}\.?\d{3}\.?\d{3}-?\d{2}'
                found_cpfs = re.findall(cpf_pattern, extracted_text)
                
                if found_cpfs:
                    # Clean the found CPFs for comparison
                    found_cpfs_clean = [re.sub(r'[^\d]', '', found_cpf) for found_cpf in found_cpfs]
                    
                    if cpf_clean in found_cpfs_clean:
                        return True, "Document validated successfully. Name and CPF match your profile."
                    else:
                        return False, "Name found but CPF in the document doesn't match your profile."
                else:
                    # If we couldn't find a CPF pattern, still accept if the name matches
                    return True, "Document partially validated. Name matches but could not verify CPF."
            else:
                # If CPF wasn't provided in personal info, accept based on name match
                return True, "Document partially validated based on name match."
        else:
            return False, "Name in the document doesn't match your profile."
    else:
        return False, "Insufficient personal information to validate document."

def find_document_type(extracted_text):
    """
    Attempt to determine the type of document from the extracted text.
    
    Args:
        extracted_text (str): Text extracted from the document image
        
    Returns:
        str: The identified document type or 'Unknown'
    """
    extracted_text = extracted_text.lower()
    
    if 'carteira de identidade' in extracted_text or 'registro geral' in extracted_text or 'rg' in extracted_text:
        return "National ID Card (RG)"
    elif 'carteira nacional de habilitação' in extracted_text or 'cnh' in extracted_text:
        return "Driver's License (CNH)"
    elif 'passaporte' in extracted_text:
        return "Passport"
    elif 'cpf' in extracted_text:
        return "CPF Card"
    else:
        return "Unknown"
