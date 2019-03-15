#!/usr/bin/env python3
import os
import sys
from pathlib import Path

dist_app_name = 'flaskbp'


def replace_within_file(path_obj, search_str, replace_str):
    with open(path_obj, 'r', encoding='utf8') as f:
        contents = f.read()

    contents = contents.replace(search_str, replace_str)

    with open(path_obj, 'w', encoding='utf8') as f:
        f.write(contents)


def check_if_rename_needed(base_dir, app_name):
    """ Compare parent and child directories to identify if a rename is
    necessary
    """
    dirs = []
    dirs.extend([d.stem for d in base_dir.glob(dist_app_name)])
    dirs.extend([d.stem for d in base_dir.glob(app_name)])

    if dist_app_name in dirs and app_name not in dirs:
        return True
    else:
        return False


def rename_app(app_name):
    """ Rename ./flaskbp to ./<app_name> """
    try:
        os.rename(dist_app_name, app_name)
    except OSError as err:
        sys.exit(err)
    except Exception as e:
        print(f'{type(e)}\n{e}')


def main():
    # Set explicit base directory
    base_dir = Path(__file__).resolve().parents[0]

    # Identify application name (parent dir name)
    app_name = base_dir.resolve().stem

    # Check if rename is needed
    rename_needed = check_if_rename_needed(base_dir, app_name)

    # Rename routine
    if rename_needed:
        rename_app(app_name)

        # Define files to exclude (exact file name match)
        blacklist_files = [
            Path(__file__).name
        ]

        # Gather file list to act on
        file_list = []
        file_list.extend(list(base_dir.glob('*.py')))
        file_list.extend(list(base_dir.glob('*/*.py')))
        file_list.extend(list(base_dir.glob('containers/*/*')))
        file_list.extend(list(base_dir.glob('docker-compose*')))

        # Replace references to dist_app_name with app_name in files
        for f in file_list:
            if f.name not in blacklist_files:
                # Imports
                dan_str = f'from {dist_app_name} import'
                an_str = f'from {app_name} import'
                replace_within_file(f, dan_str, an_str)

                dan_str = f'import {dist_app_name}'
                an_str = f'import {app_name}'
                replace_within_file(f, dan_str, an_str)

                # Common trailing patterns
                trailing = ['.', ':', '_', '/']
                for i in trailing:
                    dan_str = f'{dist_app_name}{i}'
                    an_str = f'{app_name}{i}'
                    replace_within_file(f, dan_str, an_str)

                # Common leading patterns
                leading = ['/', 'COPY ']
                for i in leading:
                    dan_str = f'{i}{dist_app_name}'
                    an_str = f'{i}{app_name}'
                    replace_within_file(f, dan_str, an_str)




if __name__ == '__main__':
    main()
