import cv2
import numpy as np
import pytesseract
from PIL import Image
import io
import re

def process_image_ocr(uploaded_file):
    """
    Processa um arquivo de imagem carregado com OCR para extrair texto.
    
    Args:
        uploaded_file: O arquivo carregado pelo Streamlit file_uploader
        
    Returns:
        str: Texto extraído da imagem
    """
    # Ler o arquivo de imagem
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    
    # Converter para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Aplicar limiar para obter imagem apenas em preto e branco
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    # Converter a imagem processada de volta para PIL Image para o tesseract
    pil_img = Image.fromarray(thresh)
    
    # Extrair texto usando tesseract
    try:
        text = pytesseract.image_to_string(pil_img, lang='por+eng')
        return text
    except Exception as e:
        print(f"Erro no processamento OCR: {e}")
        return ""

def validate_document(extracted_text, personal_info):
    """
    Valida o texto extraído de um documento comparando com as informações pessoais do usuário.
    
    Args:
        extracted_text (str): Texto extraído da imagem do documento
        personal_info (dict): Informações pessoais do usuário
        
    Returns:
        tuple: (is_valid, message) - Se o documento é válido e uma mensagem de validação
    """
    # Esta é uma validação simplificada - em uma implementação real, 
    # você usaria métodos mais sofisticados e verificação real de ID
    
    if not extracted_text:
        return False, "Não foi possível extrair texto do documento. Por favor, carregue uma imagem mais clara."
    
    # Verificar se o nome das informações pessoais aparece no documento
    name = personal_info.get('name', '').strip().lower()
    if name and len(name) > 3:  # Certificar-se de que temos um nome válido para verificar
        if name in extracted_text.lower():
            # Tentar encontrar CPF no texto extraído
            cpf = personal_info.get('cpf', '').strip()
            if cpf:
                # Remover qualquer formatação do CPF para comparação
                cpf_clean = re.sub(r'[^\d]', '', cpf)
                
                # Procurar padrão de CPF no texto
                cpf_pattern = r'\d{3}\.?\d{3}\.?\d{3}-?\d{2}'
                found_cpfs = re.findall(cpf_pattern, extracted_text)
                
                if found_cpfs:
                    # Clean the found CPFs for comparison
                    found_cpfs_clean = [re.sub(r'[^\d]', '', found_cpf) for found_cpf in found_cpfs]
                    
                    if cpf_clean in found_cpfs_clean:
                        return True, "Documento validado com sucesso. Nome e CPF correspondem ao seu perfil."
                    else:
                        return False, "Nome encontrado, mas o CPF no documento não corresponde ao seu perfil."
                else:
                    # If we couldn't find a CPF pattern, still accept if the name matches
                    return True, "Documento parcialmente validado. Nome corresponde, mas não foi possível verificar o CPF."
            else:
                # If CPF wasn't provided in personal info, accept based on name match
                return True, "Documento parcialmente validado com base na correspondência do nome."
        else:
            return False, "O nome no documento não corresponde ao seu perfil."
    else:
        return False, "Informações pessoais insuficientes para validar o documento."

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
