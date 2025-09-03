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
import logging
from flask import Blueprint
from services.authentication import authenticate
from services.cloud_storage import upload_file
from app_utils import queue_task_wrapper
from config import LOCAL_STORAGE_PATH

v1_toolkit_test_bp = Blueprint('v1_toolkit_test', __name__)
logger = logging.getLogger(__name__)

@v1_toolkit_test_bp.route('/v1/toolkit/test', methods=['GET'])
@authenticate
@queue_task_wrapper(bypass_queue=True)
def test_api(job_id, data):
    logger.info(f"Job {job_id}: Testing Ciberfobia API setup")
    
    try:
        # Create test file
        test_filename = os.path.join(LOCAL_STORAGE_PATH, "success.txt")
        with open(test_filename, 'w') as f:
            f.write("Has instalado Ciberfobia API correctamente.")
        
        # Upload file to cloud storage
        upload_url = upload_file(test_filename)
        
        # Clean up local file
        os.remove(test_filename)
        
        return upload_url, "/v1/toolkit/test", 200
        
    except Exception as e:
        logger.error(f"Job {job_id}: Error testing API setup - {str(e)}")
        return str(e), "/v1/toolkit/test", 500