from typing import List, Dict

import os
import glob
import re


def get_files(folder: str) -> List:
    return [os.path.basename(file) for file in glob.glob("{}/*.md".format(folder))]


def get_id_files_dict(files: List) -> Dict:
    return {item[:12]: item for item in files}


def get_id_title_dict(files: List) -> Dict:
    return {item[:12]: item[:-3] for item in files}


def get_links_from_file(file: str, dirname: str = "") -> List:
    file_path = "{}/{}".format(dirname, file) if dirname else file
    with open(file_path, "r") as f:
        lines = f.read()
        links = re.findall(r"\[\[(\d{12})\]\]", lines)
    return links
