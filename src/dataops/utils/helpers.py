from pathlib import Path

def ensure_directory(file_path: str):
    """Ensures that the directory for a file exists."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

def get_file_extension(file_path: str) -> str:
    """Returns the file extension."""
    return Path(file_path).suffix.lower()
