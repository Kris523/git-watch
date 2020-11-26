#!/usr/bin/python
import sys
import json
from os import path
from gDriveHandler import GAuth
DEFAULT_JSON_NAME="data.json"
DEFAULT_FOLDER_DIR="/home/eigen/Documents/git-watch/"

if len(sys.argv) < 4:
    print("Usage: python3 " + sys.argv[0] + " year month day")
    exit(1)

year = str(sys.argv[1])
month = str(sys.argv[2])
day = str(sys.argv[3])


driveHandler = GAuth()

data = driveHandler.readJsonFile("data.json")
day_all_repo_activities = data["data"][year][month][day]

day_total = 0
for repo in day_all_repo_activities.keys():
    print(repo)
    repo_total = 0
    for branch in day_all_repo_activities[repo]:
        print(branch + ": " + str(day_all_repo_activities[repo][branch]['time_delta_m']) + "m")
        repo_total += day_all_repo_activities[repo][branch]['time_delta_m']
    print("----------")
    print(repo + " total " + str(repo_total) + "m")
    print ("")
    day_total += repo_total
print("=============")
print("Days total " + str(day_total / 60) + "hr")

