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
import ffmpeg
from services.file_management import download_file
from config import LOCAL_STORAGE_PATH

def extract_thumbnail(video_url, job_id, second=0):
    """
    Extract a thumbnail from a video at the specified timestamp.
    
    Args:
        video_url (str): URL of the video to extract thumbnail from
        job_id (str): Unique identifier for the job
        second (float): Timestamp in seconds to extract the thumbnail from (default: 0)
        
    Returns:
        str: Path to the extracted thumbnail image
    """
    # Download the video from the provided URL
    video_path = download_file(video_url, os.path.join(LOCAL_STORAGE_PATH, f"{job_id}_input"))
    
    # Set output path for the thumbnail
    thumbnail_path = os.path.join(LOCAL_STORAGE_PATH, f"{job_id}_thumbnail.jpg")
    
    try:
        # Extract thumbnail using ffmpeg at the specified timestamp
        (
            ffmpeg
            .input(video_path, ss=second)  # 'ss' is the seek parameter for the timestamp
            .output(thumbnail_path, vframes=1)  # vframes=1 extracts a single frame
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        
        # Clean up the downloaded video file
        os.remove(video_path)
        
        # Ensure the thumbnail file exists
        if not os.path.exists(thumbnail_path):
            raise FileNotFoundError(f"Thumbnail file {thumbnail_path} was not created")
            
        return thumbnail_path
        
    except Exception as e:
        print(f"Thumbnail extraction failed: {str(e)}")
        # Clean up any downloaded files on error
        if os.path.exists(video_path):
            os.remove(video_path)
        raise
