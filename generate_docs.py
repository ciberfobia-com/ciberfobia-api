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
import sys
import json
import requests
import time
from pathlib import Path
from datetime import datetime, timedelta

def load_config():
    """Load configuration from env_shell.json file."""
    config_path = Path(__file__).parent / '.env_shell.json'
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            return config.get('ANTHROPIC_API_KEY'), config.get('API_DOC_OUTPUT_DIR')
    except FileNotFoundError:
        print(f"Error: Configuration file not found at: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in configuration file: {config_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading configuration: {str(e)}")
        sys.exit(1)

def load_app_context():
    """Load the app.py file from the root of the repository."""
    try:
        # Get the root directory by going up from the current file's location
        root_dir = Path(__file__).parent.parent
        app_path = Path(__file__).parent / 'app.py'
        
        if not app_path.exists():
            print("Warning: app.py not found in repository root. Documentation will be generated without API context.")
            return None
            
        with open(app_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Warning: Could not load app.py: {str(e)}")
        return None

# The prompt template to send to Claude
CLAUDE_PROMPT = '''

    Te proporciono un archivo Python que contiene definiciones de endpoints de API.
    
    Primero, aquí tienes el contexto principal de la aplicación desde app.py que muestra cómo está estructurada y gestionada la API:

** app.py abajo

{app_context}

** app.py FIN

    Ahora, lee el siguiente código del endpoint y analízalo en el contexto de la aplicación principal:

**endpoint abajo

{file_content}

    Genera documentación detallada en formato Markdown en castellano, siguiendo exactamente esta estructura:

    1. Descripción general: Explica el propósito del endpoint y cómo encaja en la estructura general de la API definida en app.py.
    2. Endpoint: Indica la ruta URL y el método HTTP.
    3. Petición:
       - Cabeceras: Lista de cabeceras necesarias (ej. x-api-key).
       - Parámetros del cuerpo: Lista de parámetros requeridos y opcionales, con tipo y propósito.
       - Analiza específicamente la directiva validate_payload en el archivo de rutas para construir la documentación.
       - Ejemplo de petición: incluye un JSON de ejemplo y un comando curl.
    4. Respuesta:
       - Respuesta de éxito: Basada en app.py y el endpoint, muestra un ejemplo completo de respuesta JSON.
       - Respuestas de error: Ejemplos de errores comunes con su código de estado y cuerpo de respuesta JSON.
    5. Manejo de errores:
       - Explica errores comunes (parámetros faltantes o inválidos, API key incorrecta, etc.) y qué códigos devuelven.
       - Incluye cualquier manejo de errores específico del contexto principal (app.py).
    6. Notas de uso: Observaciones adicionales para usar el endpoint correctamente.
    7. Problemas comunes: Lista de posibles problemas que puede encontrar un usuario.
    8. Buenas prácticas: Recomendaciones para aprovechar mejor el endpoint.
    
    Formatea con encabezados de Markdown, listas y bloques de código (json, bash). No uses introducciones ni conclusiones adicionales.
'''

def call_claude_api(message: str, api_key: str) -> str:
    """Make a direct API call to Claude."""
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }
    
    data = {
        "model": "claude-3-sonnet-20240229",
        "max_tokens": 4096,
        "temperature": 0,
        "messages": [
            {"role": "user", "content": message}
        ]
    }
    
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=data
    )
    
    if response.status_code != 200:
        raise Exception(f"API call failed with status {response.status_code}: {response.text}")
    
    return response.json()["content"][0]["text"]

def should_skip_doc_generation(output_file: Path, force: bool = False) -> bool:
    """
    Check if documentation was updated in the last 24 hours.
    
    Args:
        output_file: Path to the output markdown file
        force: If True, always return False to force generation
        
    Returns:
        bool: True if file was updated in the last 24 hours and not forced, False otherwise
    """
    # If force flag is provided, never skip
    if force:
        return False
        
    if not output_file.exists():
        return False
        
    # Get file modification time
    mod_time = datetime.fromtimestamp(output_file.stat().st_mtime)
    
    # Check if file was modified in the last 24 hours
    time_threshold = datetime.now() - timedelta(hours=24)
    
    return mod_time > time_threshold

def process_single_file(source_file: Path, output_path: Path, api_key: str, force: bool = False):
    """
    Process a single Python file.
    
    Args:
        source_file: Path to the source Python file
        output_path: Path to output the markdown file
        api_key: Anthropic API key
        force: If True, generate docs even if they were updated recently
    """
    try:
        # Create output file path
        if output_path.is_dir():
            output_file = output_path / source_file.with_suffix('.md').name
        else:
            output_file = output_path
            
        # Check if docs were recently updated
        if should_skip_doc_generation(output_file, force):
            print(f"Skipping {source_file} - documentation updated within the last 24 hours")
            return
            
        # Read the source file
        with open(source_file, 'r', encoding='utf-8') as f:
            file_content = f.read()

        # Load app.py context
        app_context = load_app_context()
        if app_context is None:
            app_context = "No app.py context available."

        # Create the full prompt
        message = CLAUDE_PROMPT.format(
            app_context=app_context,
            file_content=file_content
        )

        # Get documentation from Claude
        markdown_content = call_claude_api(message, api_key)

        # Create necessary directories
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Write the markdown content (will overwrite if exists)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        print(f"Generated documentation for: {source_file}")
        print(f"Output saved to: {output_file}")

    except Exception as e:
        print(f"Error processing {source_file}: {str(e)}", file=sys.stderr)

def process_directory(source_dir: Path, output_dir: Path, api_key: str, force: bool = False):
    """Process all Python files in the source directory recursively."""
    # Track statistics
    total_files = 0
    processed_files = 0
    skipped_files = 0
    error_files = 0
    
    start_time = time.time()
    
    # Walk through all files in source directory
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.py'):
                # Get the source file path
                source_file = Path(root) / file
                total_files += 1
                
                try:
                    # Calculate relative path to maintain directory structure
                    rel_path = source_file.relative_to(source_dir)
                    output_file = output_dir / rel_path.with_suffix('.md')

                    # Create necessary directories
                    output_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Check if we should skip this file
                    if should_skip_doc_generation(output_file, force):
                        print(f"Skipping {source_file} - documentation updated within the last 24 hours")
                        skipped_files += 1
                        continue

                    # Process the file
                    process_single_file(source_file, output_file, api_key, force)
                    processed_files += 1

                except Exception as e:
                    print(f"Error processing {source_file}: {str(e)}", file=sys.stderr)
                    error_files += 1
    
    # Print summary
    elapsed_time = time.time() - start_time
    print("\nDocumentation Generation Summary:")
    print(f"Total Python files found: {total_files}")
    print(f"Files processed: {processed_files}")
    print(f"Files skipped (updated in last 24h): {skipped_files}")
    print(f"Files with errors: {error_files}")
    print(f"Total time: {elapsed_time:.2f} seconds")

def main():
    # Check if --force flag is provided
    force_generation = False
    source_path_arg = None
    
    for arg in sys.argv[1:]:
        if arg == "--force":
            force_generation = True
        else:
            source_path_arg = arg
    
    if not source_path_arg:
        print("Usage: python script.py <source_path> [--force]")
        print("Note: source_path can be either a single .py file or a directory")
        print("Options:")
        print("  --force: Generate documentation even if it was updated within 24 hours")
        print("\nPlease ensure .env_shell.json exists in the same directory with:")
        print("  ANTHROPIC_API_KEY: Your Anthropic API key")
        print("  API_DOC_OUTPUT_DIR: Directory where documentation will be saved")
        sys.exit(1)

    # Load configuration from JSON file
    api_key, output_dir = load_config()

    # Validate configuration
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found in configuration file")
        sys.exit(1)

    if not output_dir:
        print("Error: API_DOC_OUTPUT_DIR not found in configuration file")
        sys.exit(1)

    output_path = Path(output_dir)
        
    # Get and validate source path
    source_path = Path(source_path_arg)
    
    if not source_path.exists():
        print(f"Error: Source path does not exist: {source_path}")
        sys.exit(1)

    if source_path.is_file() and not source_path.suffix == '.py':
        print("Error: Source file must be a Python file (.py)")
        sys.exit(1)

    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Starting documentation generation...")
    print(f"Source: {source_path}")
    print(f"Output: {output_path}")
    if force_generation:
        print(f"Force flag enabled: Will generate all documentation regardless of last update time.\n")
    else:
        print(f"Note: Files updated within the last 24 hours will be skipped (use --force to override).\n")
    
    # Process based on source type
    if source_path.is_file():
        # For a single file
        output_file = output_path / source_path.with_suffix('.md').name if output_path.is_dir() else output_path
        
        # Check if should skip
        if should_skip_doc_generation(output_file, force_generation):
            print(f"Skipping {source_path} - documentation updated within the last 24 hours")
        else:
            process_single_file(source_path, output_path, api_key, force_generation)
    else:
        process_directory(source_path, output_path, api_key, force_generation)

if __name__ == "__main__":
    main()