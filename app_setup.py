#!/usr/bin/env python3
import os
import sys
from pathlib import Path


def search_replace_within_file(path_obj, search_str, replace_str):
    with open(path_obj, 'r', encoding='utf8') as f:
        contents = f.read()

    contents = contents.replace(search_str, replace_str)

    with open(path_obj, 'w', encoding='utf8') as f:
        f.write(contents)


def main():
    # Set explicit base directory
    base_dir = Path(__file__).resolve().parents[0]

    # Identify application name (parent dir name) for use later
    app_name = base_dir.resolve().stem

    # Check if default name (flaskbp) exists in base_dir
    flaskbp_present = True if list(base_dir.glob('flaskbp')) != [] else False

    # Check if parent dir name matches a child dir
    app_name_present = True if list(base_dir.glob(app_name)) != [] else False

    # Flag work needed when flaskbp child path exists and mismatches parent dir
    work_needed = True if flaskbp_present and not app_name_present else False

    if not work_needed:
        help_str = 'Nothing to do!\n'
        help_str += '\tflaskbp_present: {}\n'.format(flaskbp_present)
        help_str += '\tapp_name_present: {}'.format(app_name_present)
        print(help_str)
        sys.exit(2)

    # Rename flaskbp dir to app_name
    os.rename('flaskbp', app_name)

    # Gather file list to act on
    file_list = []
    file_list.extend(list(base_dir.glob('*.py')))
    file_list.extend(list(base_dir.glob('*/*.py')))
    file_list.extend(list(base_dir.glob('containers/*/*')))
    file_list.extend(list(base_dir.glob('docker-compose*')))

    for f in file_list:
        if __file__[2:] not in str(f):
            search_replace_within_file(f, 'flaskbp', app_name)


if __name__ == '__main__':
    main()
