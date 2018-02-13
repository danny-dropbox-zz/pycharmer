#!/usr/bin/python

import string
import xml.etree.ElementTree as ET
import os

PROJECT_RELATIVE_PATH = '.idea/workspace.xml'
WORKSPACE_FILE_PATH =  '/Users/dannysi/src/server/' + PROJECT_RELATIVE_PATH

# Pretty stupid function. TODO- check if there is other way for doing this, and if we need python 3.2 for "elem.iter"
def get_sub_elem(elem, sub_elem_name):
    for sub_elem in elem.iter(sub_elem_name):
        return sub_elem

def get_file_editor_component(root):
    components = root.iterfind('component')
    for component in components:
        if component.attrib['name'] == 'FileEditorManager':
            return component

def get_open_files_paths(files_editor_manager):
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
        file_path = string.replace(file_raw_path, 'file://$PROJECT_DIR$', '~/src/server')
        file_path = string.replace(file_path, 'file://$APPLICATION_CONFIG_DIR$', '~/Library/Preferences/PyCharm2017.3')
        open_files_info.append((file_path, line))
    return open_files_info

def open_files(open_files_info):
    command = '/Applications/PyCharm.app/Contents/MacOS/pycharm ~/src/server'
    for file_path, line in open_files_info:
        command += ' --line ' + line + " " + file_path
    os.system(command)

def main():
    tree = ET.parse(WORKSPACE_FILE_PATH)
    root = tree.getroot()
    files_editor_manager = get_file_editor_component(root)
    open_files_info = get_open_files_paths(files_editor_manager)
    open_files(open_files_info)

main()