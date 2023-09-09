import os
import shutil
import subprocess
import sys
import itertools
import xml
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
repo_url = "git@github.com:omeshvalyal/helloworld.git"
local_clone_path = "/var/lib/jenkins/my_work"
source_branch_name = "master"
# current_version = "release/"+ sys.argv[2]
# print('source_branch_name: '+source_branch_name)
# print('current_version: '+current_version)
# subprocess.run(["rm", "-rf", local_clone_path])
subprocess.run(["git", "clone", "--branch", source_branch_name, "--single-branch", repo_url, local_clone_path])
# Navigate to the cloned repository
os.chdir(local_clone_path)
source_folder = "template_<version>"
destination_folder = sys.argv[2]
if os.path.exists(destination_folder) and os.path.isdir(destination_folder):
    print(f"The folder '{destination_folder}' already exists!!")
else:
    print(f"The folder '{destination_folder}' does not exist!!")
    # Copy the template version folder to the destination renaming it with current version
    shutil.copytree(source_folder, destination_folder)
    print(f"The folder '{destination_folder}' has been created!!")
source_file_list = ["changelog_"+sys.argv[1]+"_installer_isolated.xml", "changelog_"+sys.argv[1]+"_installer_mssp.xml", "changelog_"+sys.argv[1]+"_mssp.xml", "changelog_"+sys.argv[1]+".xml"]
destination_file_list = ["changelog_"+sys.argv[2]+"_installer_isolated.xml", "changelog_"+sys.argv[2]+"_installer_mssp.xml", "changelog_"+sys.argv[2]+"_mssp.xml", "changelog_"+sys.argv[2]+".xml"]
for source_file,destination_file in zip(source_file_list,destination_file_list):
    # print(source_file,destination_file)
	if os.path.exists(destination_file) and os.path.isfile(destination_file):
	    print(f"The file '{destination_file}' exists in the directory.")
	else:
	    print(f"The file '{destination_file}' does not exist in the directory!!")
	    subprocess.run(["cp", source_file, destination_file])
	    print(f"The file '{destination_file}' has been created!!")
	  
template_file_list = ["changelog_installer_isolated.xml","changelog_installer_mssp.xml","changelog_mssp.xml","changelog.xml"]
for template_source_file,destination_file in zip(template_file_list,destination_file_list):
    # Remove last tag from each file
    with open(destination_file, "r") as file:
        destination_file_content = file.read()
    modified_content = destination_file_content.replace("</databaseChangeLog>", "")
    with open(destination_file, "w") as file:
        file.write(modified_content)
    # Append the content from template file
    with open(template_source_file, "r") as file:
    	template_source_content = file.read()
    # Add one tab of indentation to each line
    indented_content = "\t" + template_source_content.replace("\n", "\n\t")
    with open(destination_file, "a") as file:
        file.write(indented_content)
    # Add the last tag back to the files
    with open(destination_file, "a") as file:
        file.write("\n</databaseChangeLog>\n")
     # replace version with actual passed version string
    with open(destination_file, "r") as file:
        destination_file_content = file.read()
    modified_content = destination_file_content.replace("current_version", sys.argv[2])
    with open(destination_file, "w") as file:
        file.write(modified_content)
# Commit the changes
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "Created folder and changelog files for "+sys.argv[2]])
# Push the changes back to the repository
subprocess.run(["git", "push"])
print("Changes pushed successfully.")
