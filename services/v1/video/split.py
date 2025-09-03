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
import subprocess
import logging
import uuid
from services.file_management import download_file
from services.cloud_storage import upload_file
from config import LOCAL_STORAGE_PATH

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def time_to_seconds(time_str):
    """
    Convert a time string in format HH:MM:SS[.mmm] to seconds.
    
    Args:
        time_str (str): Time string
        
    Returns:
        float: Time in seconds
    """
    try:
        parts = time_str.split(':')
        if len(parts) == 3:
            hours, minutes, seconds = parts
            return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
        elif len(parts) == 2:
            minutes, seconds = parts
            return int(minutes) * 60 + float(seconds)
        else:
            return float(time_str)
    except ValueError:
        raise ValueError(f"Invalid time format: {time_str}. Expected HH:MM:SS[.mmm]")

def split_video(video_url, splits, job_id=None, video_codec='libx264', video_preset='medium', 
               video_crf=23, audio_codec='aac', audio_bitrate='128k'):
    """
    Splits a video file into multiple segments with customizable encoding settings.
    
    Args:
        video_url (str): URL of the video file to split
        splits (list): List of dictionaries with 'start' and 'end' timestamps
        job_id (str, optional): Unique job identifier
        video_codec (str, optional): Video codec to use for encoding (default: 'libx264')
        video_preset (str, optional): Encoding preset for speed/quality tradeoff (default: 'medium')
        video_crf (int, optional): Constant Rate Factor for quality (0-51, default: 23)
        audio_codec (str, optional): Audio codec to use for encoding (default: 'aac')
        audio_bitrate (str, optional): Audio bitrate (default: '128k')
        
    Returns:
        tuple: (list of output file paths, input file path)
    """
    logger.info(f"Starting video split operation for {video_url}")
    if not job_id:
        job_id = str(uuid.uuid4())
        
    input_filename = download_file(video_url, os.path.join(LOCAL_STORAGE_PATH, f"{job_id}_input"))
    logger.info(f"Downloaded video to local file: {input_filename}")
    
    output_files = []
    
    try:
        # Get the file extension
        _, ext = os.path.splitext(input_filename)
        
        # Get the duration of the input file
        probe_cmd = [
            'ffprobe', 
            '-v', 'error', 
            '-show_entries', 'format=duration', 
            '-of', 'default=noprint_wrappers=1:nokey=1',
            input_filename
        ]
        duration_result = subprocess.run(probe_cmd, capture_output=True, text=True)
        
        try:
            file_duration = float(duration_result.stdout.strip())
            logger.info(f"File duration: {file_duration} seconds")
        except (ValueError, IndexError):
            logger.warning("Could not determine file duration, using a large value")
            file_duration = 86400  # 24 hours as a fallback
        
        # Validate and process splits
        valid_splits = []
        for i, split in enumerate(splits):
            try:
                start_seconds = time_to_seconds(split['start'])
                end_seconds = time_to_seconds(split['end'])
                
                # Validate split times
                if start_seconds >= end_seconds:
                    logger.warning(f"Invalid split {i+1}: start time ({split['start']}) must be before end time ({split['end']}). Skipping.")
                    continue
                
                if start_seconds < 0:
                    logger.warning(f"Split {i+1} start time {split['start']} is negative, using 0 instead")
                    start_seconds = 0
                    
                if end_seconds > file_duration:
                    logger.warning(f"Split {i+1} end time {split['end']} exceeds file duration, using file duration instead")
                    end_seconds = file_duration
                    
                # Only add valid splits
                if start_seconds < end_seconds:
                    valid_splits.append((i, start_seconds, end_seconds, split))
            except ValueError as e:
                logger.warning(f"Error processing split {i+1}: {str(e)}. Skipping.")
        
        if not valid_splits:
            raise ValueError("No valid split segments specified")
            
        logger.info(f"Processing {len(valid_splits)} valid splits")
        
        # Process each split
        for index, (split_index, start_seconds, end_seconds, split_data) in enumerate(valid_splits):
            # Create output filename for this split
            output_filename = os.path.join(LOCAL_STORAGE_PATH, f"{job_id}_split_{index+1}{ext}")
            
            # Create FFmpeg command to extract the segment
            cmd = [
                'ffmpeg',
                '-i', input_filename,
                '-ss', str(start_seconds),
                '-to', str(end_seconds),
                '-c:v', video_codec,
                '-preset', video_preset,
                '-crf', str(video_crf),
                '-c:a', audio_codec,
                '-b:a', audio_bitrate,
                '-avoid_negative_ts', 'make_zero',
                output_filename
            ]
            
            logger.info(f"Running FFmpeg command for split {index+1}: {' '.join(cmd)}")
            
            # Run the FFmpeg command
            process = subprocess.run(cmd, capture_output=True, text=True)
            
            if process.returncode != 0:
                logger.error(f"Error processing split {index+1}: {process.stderr}")
                raise Exception(f"FFmpeg error for split {index+1}: {process.stderr}")
            
            # Add the output file to the list
            output_files.append(output_filename)
            logger.info(f"Successfully created split {index+1}: {output_filename}")
        
        # Return the list of output files and the input filename
        return output_files, input_filename
        
    except Exception as e:
        logger.error(f"Video split operation failed: {str(e)}")
        
        # Clean up all temporary files if they exist
        if 'input_filename' in locals() and os.path.exists(input_filename):
            os.remove(input_filename)
                
        for output_file in output_files:
            if os.path.exists(output_file):
                os.remove(output_file)
                
        raise