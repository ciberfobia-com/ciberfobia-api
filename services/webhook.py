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

import requests
import logging

logger = logging.getLogger(__name__)

def send_webhook(webhook_url, data):
    """Send a POST request to a webhook URL with the provided data."""
    try:
        logger.info(f"Attempting to send webhook to {webhook_url} with data: {data}")
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        logger.info(f"Webhook sent: {data}")
    except requests.RequestException as e:
        logger.error(f"Webhook failed: {e}")
