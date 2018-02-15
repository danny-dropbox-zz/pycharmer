#!/usr/bin/python

import string
import xml.etree.ElementTree as ET
import os
import commands
import sys

HOME_PATH = os.path.expanduser("~")


def get_pycharm_folder():
    status, output = commands.getstatusoutput("find  ~//Library/Preferences -type d | grep -m1 PyCharm")
    return output.split('/')[-1]


# Pretty stupid function. TODO- check if there is other way for doing this, and if we need python 3.2 for "elem.iter"
def get_sub_elem(elem, sub_elem_name):
    for sub_elem in elem.iter(sub_elem_name):
        return sub_elem


def get_file_editor_component(root):
    components = root.iterfind('component')
    for component in components:
        if component.attrib['name'] == 'FileEditorManager':
            return component


def get_open_files_paths(repository_path, files_editor_manager):
    pycharm_folder = get_pycharm_folder()
    open_files_raw_paths = []
    active_file_raw_path = None
    for file in files_editor_manager.iter('file'):
        entry = file.find('entry')
        line = get_sub_elem(entry, 'caret').attrib['line']
        if file.attrib['current-in-tab'] == 'false':
            open_files_raw_paths.append((entry.attrib['file'], line))  # Adding none-active files
        else:
            active_file_raw_path = (entry.attrib['file'], line)
    if active_file_raw_path:
        open_files_raw_paths.append(active_file_raw_path)  # Adding active file (the one with focus on) at the end
    open_files_info = []
    for file_raw_path, line in open_files_raw_paths:
        file_path = string.replace(file_raw_path, 'file://$PROJECT_DIR$', '~' + repository_path)
        file_path = string.replace(file_path, 'file://$APPLICATION_CONFIG_DIR$', '~/Library/Preferences/' + pycharm_folder)
        open_files_info.append((file_path, line))
    return open_files_info


def open_files(repository_path, open_files_info):
    command = '/Applications/PyCharm.app/Contents/MacOS/pycharm ' + '~' + repository_path
    for file_path, line in open_files_info:
        command += ' --line ' + line + " " + file_path
    os.system(command)


def main():
    # calculate paths:
    repository_path = sys.argv[1]
    workspace_file_path = HOME_PATH + repository_path + '/.idea/workspace.xml'

    tree = ET.parse(workspace_file_path)
    root = tree.getroot()
    files_editor_manager = get_file_editor_component(root)
    open_files_info = get_open_files_paths(repository_path, files_editor_manager)
    open_files(repository_path, open_files_info)


main()

