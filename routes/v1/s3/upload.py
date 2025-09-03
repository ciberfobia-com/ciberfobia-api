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

from flask import Blueprint, request, jsonify
from services.authentication import authenticate
from app_utils import validate_payload, queue_task_wrapper
from services.v1.s3.upload import stream_upload_to_s3
import os
import json
import logging

logger = logging.getLogger(__name__)
v1_s3_upload_bp = Blueprint('v1_s3_upload', __name__)

@v1_s3_upload_bp.route('/v1/s3/upload', methods=['POST'])
@authenticate
@validate_payload({
    "type": "object",
    "properties": {
        "file_url": {"type": "string", "format": "uri"},
        "filename": {"type": "string"},
        "public": {"type": "boolean"},
        "download_headers": {"type": "object"}
    },
    "required": ["file_url"]
})
@queue_task_wrapper(bypass_queue=False)
def s3_upload_endpoint(job_id, data):
    try:
        file_url = data.get('file_url')
        filename = data.get('filename')  # Optional, will default to original filename if not provided
        make_public = data.get('public', False)  # Default to private
        download_headers = data.get('download_headers')  # Optional headers for authentication
        
        logger.info(f"Job {job_id}: Starting S3 streaming upload from {file_url}")
        
        # Call the service function to handle the upload
        result = stream_upload_to_s3(file_url, filename, make_public, download_headers)
        
        logger.info(f"Job {job_id}: Successfully uploaded to S3")
        
        return result, "/v1/s3/upload", 200
        
    except Exception as e:
        logger.error(f"Job {job_id}: Error streaming upload to S3 - {str(e)}")
        return str(e), "/v1/s3/upload", 500