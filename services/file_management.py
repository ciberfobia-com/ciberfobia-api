# Copyright (c) 2025 Ciberfobia
#
# Este programa es software libre: puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General de GNU (GPL), publicada
# por la Free Software Foundation, en su versión 2 o (a su elección) cualquier
# versión posterior.
#
# Este programa se distribuye con la esperanza de que sea útil, pero 
# SIN NINGUNA GARANTÍA; ni siquiera la garantía implícita de 
# COMERCIABILIDAD o IDONEIDAD PARA UN PROPÓSITO PARTICULAR.
#
# Para más detalles, consulte la Licencia Pública General de GNU.
# Debería haber recibido una copia de la misma junto con este programa;
# en caso contrario, visite: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html

import os
import uuid
import requests
from urllib.parse import urlparse, parse_qs
import mimetypes

def get_extension_from_url(url):
    """Extract file extension from URL or content type.
    
    Args:
        url (str): The URL to extract the extension from
        
    Returns:
        str: The file extension including the dot (e.g., '.jpg')
        
    Raises:
        ValueError: If no valid extension can be determined from the URL or content type
    """
    # First try to get extension from URL
    parsed_url = urlparse(url)
    path = parsed_url.path
    if path:
        ext = os.path.splitext(path)[1].lower()
        if ext:
            return ext

    # If no extension in URL, try to determine from content type
    try:
        response = requests.head(url, allow_redirects=True)
        content_type = response.headers.get('content-type', '').split(';')[0]
        ext = mimetypes.guess_extension(content_type)
        if ext:
            return ext.lower()
    except:
        pass

    # If we can't determine the extension, raise an error
    raise ValueError(f"Could not determine file extension from URL: {url}")

def download_file(url, storage_path="/tmp/"):
    """Download a file from URL to local storage."""
    # Create storage directory if it doesn't exist
    os.makedirs(storage_path, exist_ok=True)
    
    file_id = str(uuid.uuid4())
    extension = get_extension_from_url(url)
    local_filename = os.path.join(storage_path, f"{file_id}{extension}")

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        return local_filename
    except Exception as e:
        if os.path.exists(local_filename):
            os.remove(local_filename)
        raise e

