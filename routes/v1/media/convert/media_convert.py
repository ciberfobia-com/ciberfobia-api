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

from flask import Blueprint, jsonify
from app_utils import validate_payload, queue_task_wrapper
import logging
from services.v1.media.convert.media_convert import process_media_convert
from services.authentication import authenticate
from services.cloud_storage import upload_file
import os

v1_media_convert_bp = Blueprint('v1_media_convert', __name__)
logger = logging.getLogger(__name__)

@v1_media_convert_bp.route('/v1/media/convert', methods=['POST'])
@authenticate
@validate_payload({
    "type": "object",
    "properties": {
        "media_url": {"type": "string", "format": "uri"},
        "format": {"type": "string"},
        "video_codec": {"type": "string"},
        "video_preset": {"type": "string"},
        "video_crf": {"type": "number", "minimum": 0, "maximum": 51},
        "audio_codec": {"type": "string"},
        "audio_bitrate": {"type": "string"},
        "webhook_url": {"type": "string", "format": "uri"},
        "id": {"type": "string"}
    },
    "required": ["media_url", "format"],
    "additionalProperties": False
})
@queue_task_wrapper(bypass_queue=False)
def convert_media_format(job_id, data):
    media_url = data['media_url']
    output_format = data['format']
    video_codec = data.get('video_codec', 'libx264')
    video_preset = data.get('video_preset', 'medium')
    video_crf = data.get('video_crf', 23)
    audio_codec = data.get('audio_codec', 'aac')
    audio_bitrate = data.get('audio_bitrate', '128k')
    webhook_url = data.get('webhook_url')
    id = data.get('id')

    logger.info(f"Job {job_id}: Received media conversion request for media URL: {media_url} to format: {output_format}")

    try:
        output_file = process_media_convert(
            media_url, 
            job_id, 
            output_format, 
            video_codec, 
            video_preset,
            video_crf,
            audio_codec,
            audio_bitrate,
            webhook_url
        )
        logger.info(f"Job {job_id}: Media format conversion completed successfully")

        cloud_url = upload_file(output_file)
        logger.info(f"Job {job_id}: Converted media uploaded to cloud storage: {cloud_url}")
        
        return cloud_url, "/v1/media/convert", 200

    except Exception as e:
        logger.error(f"Job {job_id}: Error during media conversion process - {str(e)}")
        return {"error": str(e)}, "/v1/media/convert", 500 