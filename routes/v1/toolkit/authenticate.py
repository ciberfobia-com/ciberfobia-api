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

from flask import Blueprint, request, jsonify, current_app
from app_utils import *
from functools import wraps
import os

v1_toolkit_auth_bp = Blueprint('v1_toolkit_auth', __name__)

API_KEY = os.environ.get('API_KEY')

@v1_toolkit_auth_bp.route('/v1/toolkit/authenticate', methods=['GET'])
@queue_task_wrapper(bypass_queue=True)
def authenticate_endpoint(**kwargs):
    api_key = request.headers.get('X-API-Key')
    if api_key == API_KEY:
        return "Authorized", "/authenticate", 200
    else:
        return "Unauthorized", "/authenticate", 401
