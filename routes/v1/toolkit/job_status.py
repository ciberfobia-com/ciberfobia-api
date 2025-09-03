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
import json
import logging
from flask import Blueprint, request
from config import LOCAL_STORAGE_PATH
from services.authentication import authenticate
from app_utils import queue_task_wrapper, validate_payload

v1_toolkit_job_status_bp = Blueprint('v1_toolkit_job_status', __name__)
logger = logging.getLogger(__name__)

@v1_toolkit_job_status_bp.route('/v1/toolkit/job/status', methods=['POST'])
@authenticate
@validate_payload({
    "type": "object",
    "properties": {
        "job_id": {
            "type": "string"
        }
    },
    "required": ["job_id"],
})
@queue_task_wrapper(bypass_queue=True)
def get_job_status(job_id, data):

    get_job_id = data.get('job_id')

    logger.info(f"Retrieving status for job {get_job_id}")
    
    try:
        # Construct the path to the job status file
        job_file_path = os.path.join(LOCAL_STORAGE_PATH, 'jobs', f"{get_job_id}.json")
        
        # Check if the job file exists
        if not os.path.exists(job_file_path):
            return {"error": "Job not found", "job_id": get_job_id}, endpoint, 404
        
        # Read the job status file
        with open(job_file_path, 'r') as file:
            job_status = json.load(file)
        
        # Return the job status file content directly
        return job_status, "/v1/toolkit/job/status", 200
        
    except Exception as e:
        logger.error(f"Error retrieving status for job {get_job_id}: {str(e)}")
        return {"error": f"Failed to retrieve job status: {str(e)}"}, endpoint, 500 