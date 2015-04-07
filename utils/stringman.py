import re

def fix_path(path):
    return re.sub(r"\\", "/", path)
