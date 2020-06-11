import argparse
import os
import re

from common import get_links_from_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Zettel file.")
    parser.add_argument("--include-current", action="store_const", const=True, help="Include current name.")
    args = parser.parse_args()

    file = args.file
    if not os.path.exists(file) and not os.path.isfile(file):
        print("File not found.")

    links = get_links_from_file(file)

    if args.include_current:
        match = re.match(r"^.*(\d{12}).*\.md$", file).groups()
        if match:
            current_id = match[0]
            links.append(current_id)

    links = list(set(links))
    for link in links:
        print(link)
