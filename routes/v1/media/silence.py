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
from services.v1.media.silence import detect_silence
from services.authentication import authenticate

v1_media_silence_bp = Blueprint('v1_media_silence', __name__)
logger = logging.getLogger(__name__)

@v1_media_silence_bp.route('/v1/media/silence', methods=['POST'])
@authenticate
@validate_payload({
    "type": "object",
    "properties": {
        "media_url": {"type": "string", "format": "uri"},
        "start": {"type": "string"},
        "end": {"type": "string"},
        "noise": {"type": "string"},
        "duration": {"type": "number", "minimum": 0.1},
        "mono": {"type": "boolean"},
        "webhook_url": {"type": "string", "format": "uri"},
        "id": {"type": "string"}
    },
    "required": ["media_url", "duration"],
    "additionalProperties": False
})
@queue_task_wrapper(bypass_queue=False)
def silence(job_id, data):
    """Detect silence in a media file and return the silence intervals."""
    media_url = data['media_url']
    start_time = data.get('start', None)  # None = start from beginning
    end_time = data.get('end', None)  # None = process until end
    noise_threshold = data.get('noise', '-30dB')
    min_duration = data['duration']  # Required parameter
    mono = data.get('mono', True)  # Default to True
    
    logger.info(f"Job {job_id}: Received silence detection request for {media_url}")
    
    try:
        silence_intervals = detect_silence(
            media_url=media_url,
            start_time=start_time,
            end_time=end_time,
            noise_threshold=noise_threshold,
            min_duration=min_duration,
            mono=mono,
            job_id=job_id
        )
        
        logger.info(f"Job {job_id}: Silence detection completed successfully")
        return silence_intervals, "/v1/media/silence", 200
        
    except Exception as e:
        logger.error(f"Job {job_id}: Error during silence detection process - {str(e)}")
        return str(e), "/v1/media/silence", 500