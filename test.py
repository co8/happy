#!/usr/bin/python3

# import happy class from hap.py
from hap import happy

####
# Notes:
# To Add: Private methods, functions and data members
# _ : you shouldn’t access this method because it’s not part of the API
# __ : mangle the attribute names of a class to avoid conflicts of attribute names between classes
####

hotspot = "112MWdscG3DjHTxdCrtuLkkXNSbxCkbqkuiu8X9zFDwsBfa2teCD"
json_file = "data.json"
loadvars = {"max_activities": 25, "json_file": json_file}

activities = {
    "data": [
        {
            "version": 10010005,
            "type": "poc_request_v1",
            "time": 1630372195,
            "secret_hash": "HYQXC2J9aOkk9ZfJ-2DplWtd5jE40pmAypGhN7kiRQk",
            "onion_key_hash": "Th3aGi4Ob3uJsn2T1CvOpbuhI_efmbp5m2UTX5PsN98",
            "height": 989604,
            "hash": "FEg3PlPbwkEzYc3pVYF8Lk-lrJUB_PIf7_epTbNWpw0",
            "fee": 0,
            "challenger_owner": "14hriz8pmxm51FGmk1nuijHz6ng9z9McfJZgsg4yxzF2H7No3mH",
            "challenger_location": "8c44a111d29e3ff",
            "challenger": "112MWdscG3DjHTxdCrtuLkkXNSbxCkbqkuiu8X9zFDwsBfa2teCD",
            "block_hash": "qLXkWoGnLbJ7B8UaWIz84E72R8Sf2t3MbxYFZcrdRSU",
        }
    ],
    "cursor": "eyJtaW5fYmxvY2siOjg5NDEwOSwibWF4X2Jsb2NrIjo5ODk2MzgsImJsb2NrIjo5ODk2MDAsImFuY2hvcl9ibG9jayI6OTg5NjAwfQ",
}

# merging data and vars in loadvars
# loadvars = {**loadvars, **activities}


# Driver code
# Object instantiation
happy = happy(hotspot, json_file)  # hotspot_str_or_activities_list_or_json_file

# Accessing class attributes
# and method through objects
# print(happy.__doc__)
print(f"hotspot: {happy.hotspot}")
print(f"activities count: {len(happy.activities)}")
# print(happy.activities)
print(f"vars: {len(happy.vars)}")
# print(happy.vars)
print(f"output count: {len(happy.output)}")
