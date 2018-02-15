#!/usr/bin/python

import commands
import sys


def get_file_to_todos_dict(branch, branching_point):
    git_command = "git diff {} {}".format(branching_point, branch)
    grep_command = "grep -E '\+.*TODO|\+\+\+.*\.py'"
    status, output = commands.getstatusoutput("{} | {}".format(git_command, grep_command))
    files_and_todos_list = output.splitlines()
    line_cursor = 0
    todos_list = []
    file_name_to_todos = dict()  # TODO- change to something more efficient
    file_name = None
    while line_cursor < len(files_and_todos_list):
        line = files_and_todos_list[line_cursor]
        line_cursor += 1
        if line.find("TODO") != -1:
            todos_list.append(line)
            continue
        if line[-3:] == ".py":
            # closing last file:
            if file_name and len(todos_list):
                file_name_to_todos[file_name] = todos_list
            file_name = line.split("/", 1)[1]
            todos_list = []
    return file_name_to_todos


# TODO: check if/how we can get links in pycharm
def display_files_to_todos(file_name_to_todos):
    for file_name,todos in file_name_to_todos.iteritems():
        print("file: {} TODOs:".format(file_name))
        for todo in todos:
            print("     -{}".format(todo.split("TODO", 1)[1]))


def main():
    branch = sys.argv[1]
    branchingPoint = sys.argv[2]
    file_name_to_todos = get_file_to_todos_dict(branch, branchingPoint)
    display_files_to_todos(file_name_to_todos)


main()
