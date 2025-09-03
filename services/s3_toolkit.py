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
import boto3
import logging
from urllib.parse import urlparse, quote

logger = logging.getLogger(__name__)

def upload_to_s3(file_path, s3_url, access_key, secret_key, bucket_name, region):
    # Parse the S3 URL into bucket, region, and endpoint
    #bucket_name, region, endpoint_url = parse_s3_url(s3_url)
    
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )
    
    client = session.client('s3', endpoint_url=s3_url)

    try:
        # Upload the file to the specified S3 bucket
        with open(file_path, 'rb') as data:
            client.upload_fileobj(data, bucket_name, os.path.basename(file_path), ExtraArgs={'ACL': 'public-read'})

        # URL encode the filename for the URL
        encoded_filename = quote(os.path.basename(file_path))
        file_url = f"{s3_url}/{bucket_name}/{encoded_filename}"
        return file_url
    except Exception as e:
        logger.error(f"Error uploading file to S3: {e}")
        raise
