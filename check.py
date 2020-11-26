#!/usr/bin/python
import sys
import json
from os import path
import os
import glob, datetime, time
from pygit2 import Repository
from gDriveHandler import GAuth

DEFAULT_JSON_NAME = "data.json"
DEFAULT_FOLDER_DIR="/home/eigen/Documents/git-watch"
DEFAULT_GIT_FOLDER="/home/eigen/git/"

driveHandler = GAuth()

data = driveHandler.readJsonFile("data.json")

last_run = datetime.datetime.strptime(data["config"]["last_run"], "%d/%m/%Y %H:%M:%S")
offset = (datetime.datetime.now() - last_run)
print((offset.seconds//60)%60)
directory_contents = os.listdir(DEFAULT_GIT_FOLDER)
repos = []

for item in directory_contents:
    if os.path.isdir(DEFAULT_GIT_FOLDER + item):
        if os.path.isdir(DEFAULT_GIT_FOLDER + item + "/.git"):
            repos.append(item)
        else: # look one deeper
            sub_directory_contents = os.listdir(DEFAULT_GIT_FOLDER + item)
            for sub_item in sub_directory_contents:
                if os.path.isdir(DEFAULT_GIT_FOLDER + item +"/"+ sub_item) and  os.path.isdir(DEFAULT_GIT_FOLDER + item +"/" + sub_item + "/.git"):
                    repos.append(item +"/"+ sub_item)

accessed_within_period = []
for repo in repos:
    list_of_files = glob.glob(DEFAULT_GIT_FOLDER + repo + '/**/*', recursive=True) # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    change_time = datetime.datetime.fromtimestamp(os.path.getctime(latest_file))
    # change_time = datetime.datetime.strptime(os.path.getctime(latest_file), "%a %b %d %H:%M:%S %Y")
    if (datetime.datetime.now() - change_time < offset ):
        accessed_within_period.append(tuple((repo, latest_file )))
        print(latest_file)
        print(change_time)

#      echo "$repo_name, $branch, $DEFAULT_STEP_S, $latest_update, $current_date" >> $file/$year/$month/$day/data

num_edited_repos = len(accessed_within_period)
for newly_edited in accessed_within_period:
    repo_name = newly_edited[0]
    branch = Repository(DEFAULT_GIT_FOLDER + repo_name).head.shorthand
    latest_file = newly_edited[1]
    year, month, day = map(int, time.strftime("%Y %m %d").split())
    year = str(year)
    month = str(month)
    day = str(day)
    if(data["data"].get(year)
            and data["data"][year].get(month)
            and data["data"][year][month].get(day)
            and data["data"][year][month][day].get(repo_name)
            and data["data"][year][month][day][repo_name].get(branch)):
        current_data = data["data"][year][month][day][repo_name][branch]
        data["data"][year][month][day][repo_name][branch]["time_delta_m"] = current_data["time_delta_m"] + ((offset.seconds//60)%60)/num_edited_repos
        data["data"][year][month][day][repo_name][branch]["current_date"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data["data"][year][month][day][repo_name][branch]["lastest_update_file"] = latest_file
    else:
        #first record!
        if not data["data"].get(year):
            data["data"][year] = {}
        if not data["data"][year].get(month):
            data["data"][year][month] = {}
        if not data["data"][year][month].get(day):
            data["data"][year][month][day] = {}
        if not data["data"][year][month][day].get(repo_name):
            data["data"][year][month][day][repo_name] = {}

        data["data"][year][month][day][repo_name][branch] = {
            "repo_name": repo_name,
            "branch": branch,
            "time_delta_m": ((offset.seconds//60)%60)/num_edited_repos,
            "latest_update_time": os.path.getctime(latest_file),
            "lastest_update_file": latest_file,
            "current_date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "start_date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }

data["config"]["last_run"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
driveHandler.writeJson("data.json", data)
