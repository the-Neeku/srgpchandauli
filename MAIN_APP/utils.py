import os

def get_existing_folders(path):
    try:
        return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    except FileNotFoundError:
        return []
