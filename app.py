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

from flask import Flask, request
from queue import Queue
from services.webhook import send_webhook
import threading
import uuid
import os
import time
from version import BUILD_NUMBER  # Import the BUILD_NUMBER
from app_utils import log_job_status, discover_and_register_blueprints  # Import the discover_and_register_blueprints function

MAX_QUEUE_LENGTH = int(os.environ.get('MAX_QUEUE_LENGTH', 0))

def create_app():
    app = Flask(__name__)

    # Create a queue to hold tasks
    task_queue = Queue()
    queue_id = id(task_queue)  # Generate a single queue_id for this worker

    # Function to process tasks from the queue
    def process_queue():
        while True:
            job_id, data, task_func, queue_start_time = task_queue.get()
            queue_time = time.time() - queue_start_time
            run_start_time = time.time()
            pid = os.getpid()  # Get the PID of the actual processing thread
            
            # Log job status as running
            log_job_status(job_id, {
                "job_status": "running",
                "job_id": job_id,
                "queue_id": queue_id,
                "process_id": pid,
                "response": None
            })
            
            response = task_func()
            run_time = time.time() - run_start_time
            total_time = time.time() - queue_start_time

            response_data = {
                "endpoint": response[1],
                "code": response[2],
                "id": data.get("id"),
                "job_id": job_id,
                "response": response[0] if response[2] == 200 else None,
                "message": "success" if response[2] == 200 else response[0],
                "pid": pid,
                "queue_id": queue_id,
                "run_time": round(run_time, 3),
                "queue_time": round(queue_time, 3),
                "total_time": round(total_time, 3),
                "queue_length": task_queue.qsize(),
                "build_number": BUILD_NUMBER  # Add build number to response
            }
            
            # Log job status as done
            log_job_status(job_id, {
                "job_status": "done",
                "job_id": job_id,
                "queue_id": queue_id,
                "process_id": pid,
                "response": response_data
            })

            # Only send webhook if webhook_url has an actual value (not an empty string)
            if data.get("webhook_url") and data.get("webhook_url") != "":
                send_webhook(data.get("webhook_url"), response_data)

            task_queue.task_done()

    # Start the queue processing in a separate thread
    threading.Thread(target=process_queue, daemon=True).start()

    # Decorator to add tasks to the queue or bypass it
    def queue_task(bypass_queue=False):
        def decorator(f):
            def wrapper(*args, **kwargs):
                job_id = str(uuid.uuid4())
                data = request.json if request.is_json else {}
                pid = os.getpid()  # Get PID for non-queued tasks
                start_time = time.time()
                
                if bypass_queue or 'webhook_url' not in data:
                    
                    # Log job status as running immediately (bypassing queue)
                    log_job_status(job_id, {
                        "job_status": "running",
                        "job_id": job_id,
                        "queue_id": queue_id,
                        "process_id": pid,
                        "response": None
                    })
                    
                    response = f(job_id=job_id, data=data, *args, **kwargs)
                    run_time = time.time() - start_time
                    
                    response_obj = {
                        "code": response[2],
                        "id": data.get("id"),
                        "job_id": job_id,
                        "response": response[0] if response[2] == 200 else None,
                        "message": "success" if response[2] == 200 else response[0],
                        "run_time": round(run_time, 3),
                        "queue_time": 0,
                        "total_time": round(run_time, 3),
                        "pid": pid,
                        "queue_id": queue_id,
                        "queue_length": task_queue.qsize(),
                        "build_number": BUILD_NUMBER  # Add build number to response
                    }
                    
                    # Log job status as done
                    log_job_status(job_id, {
                        "job_status": "done",
                        "job_id": job_id,
                        "queue_id": queue_id,
                        "process_id": pid,
                        "response": response_obj
                    })
                    
                    return response_obj, response[2]
                else:
                    if MAX_QUEUE_LENGTH > 0 and task_queue.qsize() >= MAX_QUEUE_LENGTH:
                        error_response = {
                            "code": 429,
                            "id": data.get("id"),
                            "job_id": job_id,
                            "message": f"MAX_QUEUE_LENGTH ({MAX_QUEUE_LENGTH}) reached",
                            "pid": pid,
                            "queue_id": queue_id,
                            "queue_length": task_queue.qsize(),
                            "build_number": BUILD_NUMBER  # Add build number to response
                        }
                        
                        # Log the queue overflow error
                        log_job_status(job_id, {
                            "job_status": "done",
                            "job_id": job_id,
                            "queue_id": queue_id,
                            "process_id": pid,
                            "response": error_response
                        })
                        
                        return error_response, 429
                    
                    # Log job status as queued
                    log_job_status(job_id, {
                        "job_status": "queued",
                        "job_id": job_id,
                        "queue_id": queue_id,
                        "process_id": pid,
                        "response": None
                    })
                    
                    task_queue.put((job_id, data, lambda: f(job_id=job_id, data=data, *args, **kwargs), start_time))
                    
                    return {
                        "code": 202,
                        "id": data.get("id"),
                        "job_id": job_id,
                        "message": "processing",
                        "pid": pid,
                        "queue_id": queue_id,
                        "max_queue_length": MAX_QUEUE_LENGTH if MAX_QUEUE_LENGTH > 0 else "unlimited",
                        "queue_length": task_queue.qsize(),
                        "build_number": BUILD_NUMBER  # Add build number to response
                    }, 202
            return wrapper
        return decorator

    app.queue_task = queue_task

    # Register special route for Next.js root asset paths first
    from routes.v1.media.feedback import create_root_next_routes
    create_root_next_routes(app)
    
    # Use the discover_and_register_blueprints function to register all blueprints
    discover_and_register_blueprints(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)