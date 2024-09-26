import os
import shutil
from pathlib import Path

def ensure_dir(directory):
    """
    Ensure that a directory exists. If it doesn't exist, create it.
    
    Args:
    directory (str): The path to the directory.
    """
    Path(directory).mkdir(parents=True, exist_ok=True)

def list_files(directory, extensions=None):
    """
    List all files in a directory with specified extensions.
    
    Args:
    directory (str): The path to the directory.
    extensions (list): A list of file extensions to filter by. If None, all files are returned.
    
    Returns:
    list: A list of file paths.
    """
    files = []
    for file in os.listdir(directory):
        if extensions is None or any(file.endswith(ext) for ext in extensions):
            files.append(os.path.join(directory, file))
    return files

def safe_move(src, dst):
    """
    Safely move a file from src to dst. If dst already exists, it will be renamed.
    
    Args:
    src (str): The source file path.
    dst (str): The destination file path.
    """
    if os.path.exists(dst):
        base, extension = os.path.splitext(dst)
        counter = 1
        while os.path.exists(f"{base}_{counter}{extension}"):
            counter += 1
        dst = f"{base}_{counter}{extension}"
    
    shutil.move(src, dst)

def get_file_size(file_path):
    """
    Get the size of a file in bytes.
    
    Args:
    file_path (str): The path to the file.
    
    Returns:
    int: The size of the file in bytes.
    """
    return os.path.getsize(file_path)

def delete_file(file_path):
    """
    Delete a file if it exists.
    
    Args:
    file_path (str): The path to the file.
    """
    if os.path.exists(file_path):
        os.remove(file_path)

def get_file_extension(file_path):
    """
    Get the extension of a file.
    
    Args:
    file_path (str): The path to the file.
    
    Returns:
    str: The file extension (including the dot).
    """
    return os.path.splitext(file_path)[1]
