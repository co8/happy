#!/usr/bin/python3

import json

# import happy class from hap.py
from hap import happy

####
# Notes:
# To Add: Private methods, functions and data members
# _ : you shouldn’t access this method because it’s not part of the API
# __ : mangle the attribute names of a class to avoid conflicts of attribute names between classes
####

# required
hotspot = "112MWdscG3DjHTxdCrtuLkkXNSbxCkbqkuiu8X9zFDwsBfa2teCD"

# optional
loadvars = {}
json_file_input = "data.json"
data = [
    {
        "type": "rewards_v2",
        "time": 1629033433,
        "start_epoch": 966367,
        "rewards": [
            {
                "type": "poc_witnesses",
                "gateway": "112MWdscG3DjHTxdCrtuLkkXNSbxCkbqkuiu8X9zFDwsBfa2teCD",
                "amount": 879080,
                "account": "14hriz8pmxm51FGmk1nuijHz6ng9z9McfJZgsg4yxzF2H7No3mH",
            },
        ],
        "height": 966399,
        "hash": "2rsmcnn4k7uWbjCCSUu1AbMMRWlyfCp9nGCmX4jjk9A",
        "end_epoch": 966398,
    }
]

loadvars = {
    # "data": data, # 'data' from helium blockchain api response
    "json_file_input": json_file_input,  # same format as helium blockchain api response
    "json_file_output": "output.json",  # if activities, output file to write to
    # "use_cursor": True,  # in_dev
    "max_activities": 25,  # in_dev limit of activities. live or from cursor. API max ±100
}

# Object instantiation
# happy = happy(hotspot)
happy = happy(hotspot, json_file_input)
happy = happy(hotspot, loadvars)
happy = happy(hotspot, loadvars["data"])

# Accessing class attributes
# and method through objects
# print(happy.__doc__)
print(f"hotspot: {happy.hotspot}")
print(f"activities count: {len(happy.activities)}")
# print(happy.activities)
print(f"vars: {len(happy.vars)}")
# print(happy.vars)
print(f"output count: {len(happy.output)}")
# print(happy.output)
