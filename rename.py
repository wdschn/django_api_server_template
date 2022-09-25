"""
Reference:
    - https://github.com/juhanakristian/django-rename
"""

import argparse
import errno
import os
import sys
from fileinput import FileInput

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def update_project_files(path, old_name, new_name):
    """
    Updates Django project files by replacing old project name
    with the new project name.
    :param path: The project folder
    :param old_name: The old project name
    :param new_name: The new project name
    """
    manage_path = os.path.join(path, 'manage.py')
    if not os.path.exists(manage_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), manage_path)

    settings_path = os.path.join(path, 'settings', 'base.py')
    if not os.path.exists(settings_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), settings_path)

    wsgi_path = os.path.join(path, old_name, 'wsgi.py')
    if not os.path.exists(wsgi_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), wsgi_path)
    asgi_path = os.path.join(path, old_name, 'asgi.py')
    if not os.path.exists(asgi_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), wsgi_path)

    for filename in [manage_path, settings_path, wsgi_path, asgi_path]:
        with FileInput(filename, inplace=True, backup='.bak') as f:
            for line in f:
                sys.stdout.write(line.replace(old_name, new_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('new_name', type=str)
    args = parser.parse_args()

    project_folder = BASE_DIR + '/django_api_server'
    project_name = 'django_api_server'

    update_project_files(project_folder, project_name, args.new_name)

    os.rename(os.path.join(project_folder, project_name), os.path.join(project_folder, args.new_name))
    os.rename(project_folder, os.path.join(BASE_DIR, args.new_name))
