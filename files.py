import pathlib, shutil, tqdm
import contextlib, math, mmap, re, os
from pathlib import Path

def cp(src:str, dest:str)->None:
    """copy files from src (source) to dest (destination)

    Args:
        src (pathlib.Path): path of the source file
        dest (pathlib.Path): path of the destination
    """
    src = pathlib.Path(src)
    dest = pathlib.Path(dest)
    
    try:
        shutil.copy2(src, dest)
    except shutil.Error():
        print(f"ERROR: can't copy {src.name}")


def grep(filename, pattern):
    with open(filename, mode="r", encoding="utf-8") as file_obj:
        text  = file_obj.read()
        match = re.findall(pattern, text, re.M)
    
    return match


def get_cwd():
    cwd = pathlib.Path.cwd()
    
    return cwd


def search_files(type, location):
    loc = pathlib.Path(location)
    if loc.exists():
        files = list(loc.glob(f'*.{type}'))
    else:
        files = list()
        print(f"Can't open {loc}")
        
    return files


def mkdir(location: str) -> None:
    """
    Creates a directory aat the given location. Equivalent to `mkdir -p`
    If the directory already exists, no exception is raised.

    Args:
        location (str): The location where the directory should be created.

    Raises:
        Exception: An error occurred creating the directory.
    """
    loc = pathlib.Path(location)
    
    try:
        loc.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f'Cannot create {loc}! Error: {e}')


def check_file(filepath: str, create_folder: bool = False, return_status: bool = False) -> bool:
    """
    Checks if a file exists and optionally creates its parent folder and return if file exists or not.

    Args:
        filepath (str): The path of the file to check.
        create_folder (bool, optional): Create the parent folder if it doesn't exist. Defaults to False.
        return_status (bool, optional): Return the existence status of the file. Defaults to False.

    Returns:
        bool: True if the file exists and return_status is True, otherwise None.

    Raises:
        Exception: If an error occurred while checking the file or creating the directory.
    """
    try:
        file   = Path(filepath)
        folder = file.parent

        if create_folder:
            os.makedirs(folder, exist_ok=True)

        if return_status:
            return file.is_file()
    except Exception as e:
        print(f"An error occurred: {e}")


def replace_text(original_text, pattern, replacement):
    """
    Replaces all occurrences of a pattern in a string with a replacement.

    Args:
        original_text (str): The original string.
        pattern (str): The regex pattern to search for.
        replacement (str): The text to replace the pattern with.

    Returns:
        str: The string with all occurrences of the pattern replaced.

    Example:
        >>> replace_text("Hello, world! Hello, world!", "world", "Python")
        'Hello, Python! Hello, Python!'
    """
    updated_text = re.sub(pattern, replacement, original_text)
    
    return updated_text
