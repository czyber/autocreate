import os

import shutil


def cleanup_dir(directory: str):
    if os.path.exists(directory):
        shutil.rmtree(directory)
