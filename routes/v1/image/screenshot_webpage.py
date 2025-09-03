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
from app_utils import *
from app_utils import validate_payload, queue_task_wrapper
import logging
import os
from services.v1.image.screenshot_webpage import take_screenshot
from services.authentication import authenticate
from services.cloud_storage import upload_file
from playwright.sync_api import sync_playwright
from io import BytesIO


v1_image_screenshot_webpage_bp = Blueprint('v1_image_screenshot_webpage', __name__)
logger = logging.getLogger(__name__)


@v1_image_screenshot_webpage_bp.route('/v1/image/screenshot/webpage', methods=['POST'])
@authenticate
@validate_payload({
    "type": "object",
    "properties": {
        "url": {"type": "string", "format": "uri"},
        "html": {"type": "string"},
        "viewport_width": {"type": "integer", "minimum": 1},
        "viewport_height": {"type": "integer", "minimum": 1},
        "full_page": {"type": "boolean", "default": False},
        "format": {"type": "string", "enum": ["png", "jpeg"], "default": "png"},
        "delay": {"type": "integer", "minimum": 0},
        "device_scale_factor": {"type": "number", "minimum": 0.1},
        "user_agent": {"type": "string"},
        "cookies": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "value", "domain"],
                "properties": {
                    "name": {"type": "string"},
                    "value": {"type": "string"},
                    "domain": {"type": "string"},
                    "path": {"type": "string", "default": "/"},
                },
                "additionalProperties": True
            }
        },
        "headers": {
            "type": "object",
            "additionalProperties": {"type": "string"}
        },
        "quality": {"type": "integer", "minimum": 0, "maximum": 100},
        "clip": {
            "type": "object",
            "required": ["x", "y", "width", "height"],
            "properties": {
                "x": {"type": "number"},
                "y": {"type": "number"},
                "width": {"type": "number", "exclusiveMinimum": 0},
                "height": {"type": "number", "exclusiveMinimum": 0}
            }
        },
        "timeout": {"type": "integer", "minimum": 100},
        "wait_until": {"type": "string", "enum": ["load", "domcontentloaded", "networkidle", "networkidle2"], "default": "load"},
        "wait_for_selector": {"type": "string"},
        "emulate": {
            "type": "object",
            "properties": {
                "color_scheme": {
                    "type": "string",
                    "enum": ["light", "dark"]
                }
            }
        },
        "omit_background": {"type": "boolean", "default": False},
        "selector": {"type": "string"},
        "js": {"type": "string"},
        "css": {"type": "string"},
        "webhook_url": {"type": "string", "format": "uri"},
        "id": {"type": "string"}
    },
    "oneOf": [
        {"required": ["url"]},
        {"required": ["html"]}
    ],
    "not": {"required": ["url", "html"]},
    "additionalProperties": False
})
@queue_task_wrapper(bypass_queue=False)
def screenshot(job_id, data):
    logger.info(f"Job {job_id}: Received screenshot request for {data.get('url')}")
    try:
        screenshot_io = take_screenshot(data, job_id)
        if isinstance(screenshot_io, dict) and 'error' in screenshot_io:
            logger.error(f"Job {job_id}: Screenshot error: {screenshot_io['error']}")
            return {"error": screenshot_io['error']}, "/v1/image/screenshot/webpage", 400
        format = data.get("format", "png")
        temp_file_path = f"{job_id}_screenshot.{format}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(screenshot_io.read())
        cloud_url = upload_file(temp_file_path)
        os.remove(temp_file_path)
        logger.info(f"Job {job_id}: Screenshot successfully processed and uploaded.")
        return cloud_url, "/v1/image/screenshot/webpage", 200
    except Exception as e:
        logger.error(f"Job {job_id}: Error processing screenshot: {str(e)}", exc_info=True)
        return {"error": str(e)}, "/v1/image/screenshot/webpage", 500