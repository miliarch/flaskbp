#!/usr/bin/env python3
import os
import shutil
import sys
from pathlib import Path


def check_if_rename_needed(base_dir, old_path, new_path):
    """ Compare parent and child directories to identify if a rename is
    necessary
    """
    dirs = []
    dirs.extend([d.name for d in base_dir.glob(old_path.name)])
    dirs.extend([d.name for d in base_dir.glob(new_path.name)])

    if old_path.name in dirs and new_path.name not in dirs:
        return True
    else:
        return False


def copy_file(original_path, target_path, overwrite=False):
    """ Copy original_path to target_path """
    if overwrite or not target_path.exists():
        try:
            shutil.copy(str(original_path), str(target_path))
            return True
        except IOError as err:
            sys.exit(err)
    else:
        return False


def rename_app(old_path, new_path):
    """ Rename old_path to new_path """
    try:
        os.rename(str(old_path), str(new_path))
    except OSError as err:
        sys.exit(err)
    except Exception as e:
        sys.exit('{}\n{}'.format(type(e), e))


def replace_within_file(file_path, search_str, replace_str):
    """ Replace search_str with replace_str within file_path """
    with open(str(file_path), 'r', encoding='utf8') as f:
        contents = f.read()

    contents = contents.replace(search_str, replace_str)

    with open(str(file_path), 'w', encoding='utf8') as f:
        f.write(contents)


def main():
    # Set explicit base directory
    base_dir = Path(__file__).resolve().parents[0]

    # Set distributed app name
    dist_app_name = 'flaskbp'

    # Identify application name (parent dir name)
    app_name = base_dir.resolve().name

    # Check if rename is needed
    old_path = Path('{}/{}'.format(base_dir, dist_app_name))
    new_path = Path('{}/{}'.format(base_dir, app_name))
    rename_needed = check_if_rename_needed(base_dir, old_path, new_path)

    # Rename routine
    if rename_needed:
        status_str = 'Renaming {} to {}\n'.format(old_path, new_path)
        print(status_str)
        rename_app(old_path, new_path)

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
        status_str = 'Replacing references to {} in files:'.format(
            dist_app_name)
        print(status_str)
        for f in file_list:
            if f.name not in blacklist_files:
                status_str = '  - {}'.format(f.resolve())
                print(status_str)
                # Imports
                dan_str = 'from {} import'.format(dist_app_name)
                an_str = 'from {} import'.format(app_name)
                replace_within_file(f, dan_str, an_str)

                dan_str = 'import {}'.format(dist_app_name)
                an_str = 'import {}'.format(app_name)
                replace_within_file(f, dan_str, an_str)

                # Common trailing patterns
                trailing = ['.', ':', '_', '/']
                for i in trailing:
                    dan_str = '{}{}'.format(dist_app_name, i)
                    an_str = '{}{}'.format(app_name, i)
                    replace_within_file(f, dan_str, an_str)

                # Common leading patterns
                leading = ['/', 'COPY ']
                for i in leading:
                    dan_str = '{}{}'.format(i, dist_app_name)
                    an_str = '{}{}'.format(i, app_name)
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
        original_path = Path('{}/{}'.format(base_dir, key))
        target_path = Path('{}/{}'.format(base_dir, config_file_map[key]))
        success = copy_file(original_path, target_path)
        success_str = '  + ' if success else '  X '
        if success:
            success_str += '{} -> {}'.format(original_path, target_path)
        else:
            success_str += '{} could not be created '.format(target_path)
            success_str += '(file exists or other error)'
        print('{}'.format(success_str))
    print()

    # Create data and logs directories
    new_dirs = [
        'data',
        'logs'
    ]

    status_str = 'Creating default directories:'
    print(status_str)
    for d in new_dirs:
        d = Path('{}/{}'.format(base_dir, d))
        status_str = ''
        try:
            d.mkdir()
            status_str += '  + {} created'.format(d)
        except FileExistsError as err:
            status_str += '  X {} could not be created ({})'.format(d, err)
        except Exception as e:
            status_str += '  X {} could not be created ({})'.format(d, e)
        print(status_str)
    print()


if __name__ == '__main__':
    main()
    print('DONE')
