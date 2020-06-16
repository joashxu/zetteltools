from typing import List, Dict
import os
import json
import argparse
import sys
from string import Template

from common import get_files, get_links_from_file, get_id_files_dict, get_id_title_dict


FORCE_GRAPH_TEMPLATE_NAME = "force_graph.html"
OUTPUT_FILE_NAME = "output.html"


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
    parser.add_argument("--highlight", nargs='*', help="Highlight zettel ID")
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

    highlight = []
    if args.highlight is not None:
        highlight = args.highlight if args.highlight else []
        if not highlight:
            highlight = [line.strip() for line in sys.stdin]

    generate_force_graph(id_files_dict, id_title_dict, dirname, highlight=highlight)
