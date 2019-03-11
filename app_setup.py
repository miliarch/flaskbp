#!/usr/bin/env python3
import os
import sys
from pathlib import Path


def search_replace_within_file(path_obj, search_str, replace_str):
    with open(path_obj, 'r') as f:
        contents = f.read()

    contents = contents.replace(search_str, replace_str)

    with open(path_obj, 'w') as f:
        f.write(contents)


def main():
    # Set explicit base directory
    base_dir = Path(__file__).resolve().parents[0]

    # Identify application name (parent dir name) for use later
    app_name = base_dir.resolve().stem

    # Check if default name (funnyman) exists in base_dir
    funnyman_present = True if list(base_dir.glob('funnyman')) != [] else False

    # Check if parent dir name matches a child dir
    app_name_present = True if list(base_dir.glob(app_name)) != [] else False

    # Flag work needed when funnyman child path exists and mismatches parent dir
    work_needed = True if funnyman_present and not app_name_present else False

    if not work_needed:
        help_str = 'Nothing to do!\n'
        help_str += '\tfunnyman_present: {}\n'.format(funnyman_present)
        help_str += '\tapp_name_present: {}'.format(app_name_present)
        print(help_str)
        sys.exit(2)

    # Rename funnyman dir to app_name
    os.rename('funnyman', app_name)

    # Find python files to update references in
    python_files = list(base_dir.glob('*.py'))
    python_files.extend(list(base_dir.glob('*/*.py')))

    for pf in python_files:
        search_replace_within_file(pf, 'flaskbp', app_name)



if __name__ == '__main__':
    main()
