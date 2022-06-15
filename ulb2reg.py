#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Converts a ULB project in BTT-Writer or translationStudio to a REG project.
Updates the manifest with the new information, and renames the project folder.

Created on Wed 15 Jun 2022 02:56:09 PM EDT

Version: 0.01

@author: jdwood
"""

import argparse
import os.path
import json
import re

parser = argparse.ArgumentParser(description="Convert translationStudio or BTT-Writer project from ULB to REG")
parser.add_argument("project_path", help="Path to the project to be converted")

args = parser.parse_args()

# Input
PROJECT_PATH = args.project_path

def convert_ulb_to_reg(passed_project_path):
    print("You are trying to convert "+passed_project_path)
    check_for_valid_project(passed_project_path)

def updateManifestFile(filePath):
    with open(filePath) as manifestFile:
        manifestContent = json.load(manifestFile)
        manifestFile.close()
        for key, value in manifestContent.items():
            print(key,"\n")
        if manifestContent["resource"]["id"] == "ulb":
            print("Yup, the manifest says this is a ULB project.")
            manifestContent["resource"]["id"] = "reg"
            manifestContent["resource"]["name"] = "Regular"

        print(json.dumps(manifestContent,indent=4))

        with open(filePath, "w") as manifestFile:
            json.dump(manifestContent,manifestFile,ensure_ascii=False, indent=4)
            manifestFile.close()

def renameFolder(folderPath):
    newName = re.sub(r"_ulb$","_reg",folderPath)
    os.rename(folderPath, newName)

def check_for_valid_project(passed_path):
    if os.path.exists(passed_path):
        theAbsPath = os.path.abspath(passed_path)
        print("I think the path is: "+theAbsPath)
        if theAbsPath[-4:] == "_ulb":
            print("This looks like a ulb project")
            manifestPath = theAbsPath+"/manifest.json"
            if os.path.exists(manifestPath):
                print("... and I think the manifest file exists")
                updateManifestFile(manifestPath)
                renameFolder(theAbsPath)
            else:
                print("... but there doesn't seem to be a manifest file.")
        else:
            print("The last four characters of the path are "+theAbsPath[-4:])
            print("This doesn't seem to be a ulb project, based upon the folder name.")
    else:
        print("This doesn't seem to be a valid folder path. A project is a folder.")

def main():
    print("ULB to REG Converter")
    convert_ulb_to_reg(PROJECT_PATH)

if __name__ == "__main__":
    main()
