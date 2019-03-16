#!/usr/bin/env python3
import os
import shutil
import sys
from pathlib import Path


def check_if_rename_needed(base_dir, dist_app_name, app_name):
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


def copy_file(original, target, overwrite=False):
    """ Copy file original to target """
    original = Path(original)
    target = Path(target)

    if overwrite or not target.exists():
        try:
            shutil.copy(original.name, target.name)
            return True
        except IOError as err:
            sys.exit(err)
    else:
        return False


def rename_app(dist_app_name, app_name):
    """ Rename ./<dist_app_name> to ./<app_name> """
    try:
        os.rename(dist_app_name, app_name)
    except OSError as err:
        sys.exit(err)
    except Exception as e:
        sys.exit(f'{type(e)}\n{e}')


def replace_within_file(path_obj, search_str, replace_str):
    """ Replace search_string with replace_str within path_obj file """
    with open(path_obj, 'r', encoding='utf8') as f:
        contents = f.read()

    contents = contents.replace(search_str, replace_str)

    with open(path_obj, 'w', encoding='utf8') as f:
        f.write(contents)


def main():
    # Set explicit base directory
    base_dir = Path(__file__).resolve().parents[0]

    # Set distributed app name
    dist_app_name = 'flaskbp'

    # Identify application name (parent dir name)
    app_name = base_dir.resolve().stem

    # Check if rename is needed
    rename_needed = check_if_rename_needed(base_dir, dist_app_name, app_name)

    # Rename routine
    if rename_needed:
        rename_app(dist_app_name, app_name)

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
        status_str = f'Replacing references to {dist_app_name} in files:'
        print(status_str)
        for f in file_list:
            if f.name not in blacklist_files:
                status_str = f'  - {f.resolve()}'
                print(status_str)
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
        print()

    # Copy config files from examples
    # Map "example config": "config"
    config_file_map = {
        'config.py.example': 'config.py',
        'docker-compose.yml.dev.example': 'docker-compose.yml'
    }

    status_str = "Copying config example files:"
    print(status_str)
    for key in config_file_map.keys():
        success = copy_file(key, config_file_map[key])
        success_str = '+ ' if success else 'X '
        if success:
            success_str += f'{key} -> {config_file_map[key]}'
        else:
            success_str += f'{config_file_map[key]} could not be created'
            success_str += f'(file exists or other error)'
        print(f'{success_str}')
    print()


    # Create data and logs directories
    new_dirs = [
        'data',
        'logs'
    ]

    status_str = f'Creating default directories:'
    print(status_str)
    for d in new_dirs:
        d = Path(d)
        status_str = ''
        try:
            d.mkdir()
            status_str += f'+ {d.resolve()} created'
        except FileExistsError as err:
            status_str += f'X {d.resolve()} could not be created ({err})'
        except Exception as e:
            status_str += f'X {d.resolve()} could not be created ({e})'
        print(status_str)
    print()


if __name__ == '__main__':
    main()
    print('DONE')
