import os
import subprocess

def check_root_permissions():
    """
    Verifica si el script se está ejecutando como root.
    """
    if os.geteuid() != 0:
        raise PermissionError("Este script debe ejecutarse como usuario root.")

def run_command(command: list, capture_output: bool = False):
    """
    Ejecuta un comando en la terminal.
    :param command: Lista que representa el comando y sus argumentos.
    :param capture_output: Si se debe capturar la salida del comando.
    :return: Salida del comando si capture_output es True.
    """
    try:
        if capture_output:
            result = subprocess.run(command, check=True, text=True, capture_output=True)
            return result.stdout.strip()
        else:
            subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error al ejecutar el comando {' '.join(command)}: {str(e)}")

def file_exists(file_path: str) -> bool:
    """
    Verifica si un archivo existe en el sistema.
    :param file_path: Ruta del archivo.
    :return: True si el archivo existe, False en caso contrario.
    """
    return os.path.isfile(file_path)

def read_file(file_path: str) -> str:
    """
    Lee el contenido de un archivo.
    :param file_path: Ruta del archivo.
    :return: Contenido del archivo como una cadena de texto.
    """
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo {file_path} no fue encontrado.")
    except Exception as e:
        raise RuntimeError(f"Error al leer el archivo {file_path}: {str(e)}")

def write_file(file_path: str, content: str):
    """
    Escribe contenido en un archivo.
    :param file_path: Ruta del archivo.
    :param content: Contenido a escribir en el archivo.
    """
    try:
        with open(file_path, "w") as file:
            file.write(content)
    except Exception as e:
        raise RuntimeError(f"Error al escribir en el archivo {file_path}: {str(e)}")
