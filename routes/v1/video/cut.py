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

from flask import Blueprint
from app_utils import *
import logging
from services.v1.video.cut import cut_media
from services.authentication import authenticate

v1_video_cut_bp = Blueprint('v1_video_cut', __name__)
logger = logging.getLogger(__name__)

@v1_video_cut_bp.route('/v1/video/cut', methods=['POST'])
@authenticate
@validate_payload({
    "type": "object",
    "properties": {
        "video_url": {"type": "string", "format": "uri"},
        "cuts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "start": {"type": "string"},
                    "end": {"type": "string"}
                },
                "required": ["start", "end"],
                "additionalProperties": False
            },
            "minItems": 1
        },
        "video_codec": {"type": "string"},
        "video_preset": {"type": "string"},
        "video_crf": {"type": "number", "minimum": 0, "maximum": 51},
        "audio_codec": {"type": "string"},
        "audio_bitrate": {"type": "string"},
        "webhook_url": {"type": "string", "format": "uri"},
        "id": {"type": "string"}
    },
    "required": ["video_url", "cuts"],
    "additionalProperties": False
})
@queue_task_wrapper(bypass_queue=False)
def video_cut(job_id, data):
    """Cut specified segments from a video file with optional encoding settings."""
    video_url = data['video_url']
    cuts = data['cuts']
    
    # Extract encoding settings with defaults
    video_codec = data.get('video_codec', 'libx264')
    video_preset = data.get('video_preset', 'medium')
    video_crf = data.get('video_crf', 23)
    audio_codec = data.get('audio_codec', 'aac')
    audio_bitrate = data.get('audio_bitrate', '128k')
    
    logger.info(f"Job {job_id}: Received video cut request for {video_url}")
    
    try:
        # Process the video file and get local file paths
        output_filename, input_filename = cut_media(
            video_url=video_url,
            cuts=cuts,
            job_id=job_id,
            video_codec=video_codec,
            video_preset=video_preset,
            video_crf=video_crf,
            audio_codec=audio_codec,
            audio_bitrate=audio_bitrate
        )
        
        # Upload the processed file to cloud storage
        from services.cloud_storage import upload_file
        cloud_url = upload_file(output_filename)
        logger.info(f"Job {job_id}: Uploaded output to cloud: {cloud_url}")
        
        # Clean up temporary files
        import os
        os.remove(input_filename)
        os.remove(output_filename)
        logger.info(f"Job {job_id}: Removed temporary files")
        
        logger.info(f"Job {job_id}: Video cut operation completed successfully")
        return cloud_url, "/v1/video/cut", 200
        
    except Exception as e:
        logger.error(f"Job {job_id}: Error during video cut process - {str(e)}")
        return str(e), "/v1/video/cut", 500