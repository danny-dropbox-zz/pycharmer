#!/usr/bin/python
import sys
import os
from shutil import copyfile

def dir_exists(dir):
	#print(os.path.isdir(main_dir) , os.path.exists(main_dir))
	return os.path.isdir(dir) and os.path.exists(dir)

def make_dir_if_not_exists(dir):
	if not dir_exists(dir):
		os.mkdir(dir)

home = os.path.expanduser("~")
main_dir = home+'/.pycharm-switcher'
make_dir_if_not_exists(main_dir)
_, prevBranch, newBranch, root_dir = sys.argv
root_dir = os.path.dirname(os.path.dirname(root_dir))
prevDir= main_dir+"/"+prevBranch
make_dir_if_not_exists(prevDir)
workspace_dir=root_dir+"/.idea"
workspace_file = workspace_dir+"/workspace.xml"
copyfile(workspace_file,prevDir+"/workspace.xml")
new_workspace_file = main_dir+"/"+newBranch+"/workspace.xml"
if os.path.exists(new_workspace_file):
	copyfile(new_workspace_file, workspace_file)
sys.exit(0)

