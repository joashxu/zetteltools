from typing import List, Dict

import os
import glob
import re
import json
import argparse

from string import Template

FORCE_GRAPH_TEMPLATE_NAME = "force_graph.html"
OUTPUT_FILE_NAME = "output.html"


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


def generate_force_graph(id_files_dict: Dict, id_title_dict: Dict, dirname: str = "", highlight: List = None) -> None:
    if not highlight:
        highlight = []

    # Create nodes
    # Dict(id, group)
    nodes = [
        {"id": title, "group": 2 if uid in highlight else 1}
        for uid, title in id_title_dict.items()
    ]

    # Create links
    # Dict(source, target, value)
    links = []
    for uid, file in id_files_dict.items():
        file_links = get_links_from_file(file, dirname=dirname)
        link_list = [
            {"source": id_title_dict[uid], "target": id_title_dict[link], "value": 2}
            for link in file_links
            if id_title_dict.get(link, None)
        ]
        links.extend(link_list)

    # Create Output and open it
    data = json.dumps({"nodes": nodes, "links": links})
    with open(FORCE_GRAPH_TEMPLATE_NAME, "r") as f:
        template = f.read()
        s = Template(template)
        with open(OUTPUT_FILE_NAME, "w") as out:
            out.write(s.substitute(data=data))

    os.system("open {}".format(OUTPUT_FILE_NAME))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "directory", help="Source Directory (Default to current directory)"
    )
    parser.add_argument("--highlight", help="Starts from current zettel ID")
    args = parser.parse_args()

    dirname = args.directory
    if not os.path.isdir(dirname):
        print("Invalid directory, please check you directory")
        exit(1)

    # Handle the file
    files = get_files(dirname)
    if not files:
        print("No markdown file found.")
        exit(1)

    # Create title and files map
    id_files_dict = get_id_files_dict(files)
    id_title_dict = get_id_title_dict(files)

    if not id_files_dict or not id_title_dict:
        print("No valid Zettel was found.")
        exit(1)

    highlight = args.highlight if args.highlight else []
    generate_force_graph(id_files_dict, id_title_dict, dirname, highlight=highlight)
