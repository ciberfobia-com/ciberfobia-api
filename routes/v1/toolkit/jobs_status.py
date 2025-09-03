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
import time
from flask import Blueprint, request
from config import LOCAL_STORAGE_PATH
from services.authentication import authenticate
from app_utils import queue_task_wrapper, validate_payload

v1_toolkit_jobs_status_bp = Blueprint('v1_toolkit_jobs_status', __name__)
logger = logging.getLogger(__name__)

@v1_toolkit_jobs_status_bp.route('/v1/toolkit/jobs/status', methods=['POST'])
@authenticate
@queue_task_wrapper(bypass_queue=True)
def get_all_jobs_status(job_id, data):
    """
    Get the status of all jobs within a specified time range
    
    Args:
        job_id (str): Job ID assigned by queue_task_wrapper (unused)
        data (dict): Request data containing optional since_seconds parameter
    
    Returns:
        Tuple of (jobs_status_data, endpoint_string, status_code)
    """
    logger.info("Retrieving status for all jobs")
    endpoint = "/v1/toolkit/jobs/status"
    
    try:
        # Get time range parameter (default to 600 seconds/10 minutes if not provided)
        since_seconds = 600
        if data and "since_seconds" in data:
            since_seconds = data.get("since_seconds")
            
        cutoff_time = time.time() - since_seconds
        
        # Construct the path to the jobs directory
        jobs_dir = os.path.join(LOCAL_STORAGE_PATH, 'jobs')
        
        # Check if the jobs directory exists
        if not os.path.exists(jobs_dir):
            return {"error": "Jobs directory not found"}, endpoint, 404
        
        # Dictionary to store job statuses
        jobs_status = {}
        
        # Iterate through job files in the directory
        for filename in os.listdir(jobs_dir):
            if filename.endswith('.json'):
                job_file_path = os.path.join(jobs_dir, filename)
                file_mod_time = os.path.getmtime(job_file_path)
                
                # Check if the file was modified within the time range
                if file_mod_time >= cutoff_time:
                    job_id = filename.split('.')[0]  # Remove .json extension to get job_id
                    
                    # Read the job status file
                    with open(job_file_path, 'r') as file:
                        job_data = json.load(file)
                        
                        # Only include the job_status field, not the response
                        if "job_status" in job_data:
                            jobs_status[job_id] = job_data["job_status"]
        
        # Return the job statuses
        return jobs_status, endpoint, 200
        
    except Exception as e:
        logger.error(f"Error retrieving status for jobs: {str(e)}")
        return {"error": f"Failed to retrieve job statuses: {str(e)}"}, endpoint, 500 