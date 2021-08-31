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
# loadvars = {}
# data_empty = [{}]
data_list = [
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
json_file_input = "data.json"
loadvars = {
    # "data": data_list,  # 'data' from helium blockchain api response
    "json_file_input": json_file_input,  # same format as helium blockchain api response
    "json_file_output": "output.json",  # if activities, output file to write to
    # "get_fresh_cursor_and_use_to_get_activities": True,
    # "cursor": "eyJ0eG4iOiJ6aFh6TWJTQlBLVVpkWVIxRjlITHNkQm9CeC01ZzV2TVVUZzREMkxFVzBzIiwibWluX2Jsb2NrIjo4OTQxMDksIm1heF9ibG9jayI6OTY2NTg5LCJibG9jayI6OTYyNTUyLCJhbmNob3JfYmxvY2siOjk2NjUwMH0",
    # "max": 25,  # limit number of activities. live or from cursor. API max ±100
    "get_hotspot_data": False,  # in_dev
    "get_wallet_balance": False,  # in_dev
}

### Object instantiation
# happy = happy(hotspot)
# happy = happy(hotspot, loadvars)
# happy = happy(hotspot, json_file_input)
happy = happy(hotspot, data_list)

## Objects
# happy.hotspot
# happy.activities  # incoming activities
# happy.ness  # happy parsed activities
# happy.vars  # dict of happy vars


# Accessing class attributes
# and method through objects
# print(happy.__doc__)
print(f"hotspot: {happy.hotspot}")
print(f"activities count: {len(happy.activities)}")
# print(happy.activities)
print(f"vars: {len(happy.vars)}")
# print(happy.vars)
print(f"happy.ness count: {len(happy.ness)}")
print(happy.ness[0]["name"])
print(happy.ness[0]["emoji"])
# print(happy.output)
