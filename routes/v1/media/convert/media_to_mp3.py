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

from flask import Blueprint, current_app
from app_utils import *
import logging
from services.v1.media.convert.media_to_mp3 import process_media_to_mp3
from services.authentication import authenticate
from services.cloud_storage import upload_file
import os

v1_media_convert_mp3_bp = Blueprint('v1_media_convert_mp3', __name__)
logger = logging.getLogger(__name__)

@v1_media_convert_mp3_bp.route('/v1/media/convert/mp3', methods=['POST'])
@v1_media_convert_mp3_bp.route('/v1/media/transform/mp3', methods=['POST']) #depleft for backwards compatibility, do not use.
@authenticate
@validate_payload({
    "type": "object",
    "properties": {
        "media_url": {"type": "string", "format": "uri"},
        "webhook_url": {"type": "string", "format": "uri"},
        "id": {"type": "string"},
        "bitrate": {"type": "string", "pattern": "^[0-9]+k$"},
        "sample_rate": {"type": "number"}
    },
    "required": ["media_url"],
    "additionalProperties": False
})
@queue_task_wrapper(bypass_queue=False)
def convert_media_to_mp3(job_id, data):
    media_url = data['media_url']
    webhook_url = data.get('webhook_url')
    id = data.get('id')
    bitrate = data.get('bitrate', '128k')
    sample_rate = data.get('sample_rate')

    logger.info(f"Job {job_id}: Received media-to-mp3 request for media URL: {media_url}")

    try:
        output_file = process_media_to_mp3(media_url, job_id, bitrate, sample_rate)
        logger.info(f"Job {job_id}: Media conversion process completed successfully")

        cloud_url = upload_file(output_file)
        logger.info(f"Job {job_id}: Converted media uploaded to cloud storage: {cloud_url}")

        return cloud_url, "/v1/media/transform/mp3", 200

    except Exception as e:
        logger.error(f"Job {job_id}: Error during media conversion process - {str(e)}")
        return str(e), "/v1/media/transform/mp3", 500