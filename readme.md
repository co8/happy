# HAPpy - Helium API Parser, Python

### Easily Access Helium Blockchain API Data with just your Hotspot Address

<!-- **Listed as a Helium Community Tool** [https://explorer.helium.com/tools](https://explorer.helium.com/tools) -->

```PYTHON
# Import
from hap import happy

# Hotspot Address
hotspot_address = "112MWdscG3DjHTxdCrtuLkkXNSbxCkbqkuiu8X9zFDwsBfa2teCD"

# Instantiate HAPpy
happy = happy(hotspot_address)

# Response Object
print(happy.ness)

# happy.ness Output
[
  {
    "height": 966398,
    "hash": "ONGyfDAfMQL8gVMPFqUEypxVIjz_l7jxTvG9D2_NkRc",
    "time": 1629033383,
    "time_nice": "09:16 15/AUG",
    "type": "poc_receipts_v1",
    "subtype": "valid_witness",
    "emoji": "🛸",
    "name": "Valid Witness",
    "witnesses": 25,
    "witness_text": "Witnesses",
    "valid_witnesses": 20
  },
]
```

🛸 Valid Witness, 1 of 25, 20 Valid Witnesses, 09:16 15/AUG at height 966,398

---

#### Features

- Uses [Helium Blockchain API](https://docs.helium.com/api/blockchain/introduction/)
- Python 3.9+
- Easy to use Response
- Options:
  - Current Activities or with Pagination/Cursor
  - Input JSON file or Object
  - Write Response to JSON file
  - Filter by Type and Subtype (rewards_v2, rewards_beacon)
  - Set Maximum
  - Get Hotspot Data
  - Get Wallet Data
- Parsed and Formatted Data
  - Name of Activity Type
  - Reward Amounts and Types
  - Subtypes for easy filtering (valid_witness, sent_beacon, rewards_challenger)
  - HNT format amounts for Regular and Micropayments
  - Pluralized Words
  - Formatted Date/Time
  - Emoji's for each Activity Type and HNT
- Activities are provided with additional Contextual Information
  - Number of Total and Valid Witnesses for Beacons and Challenges
  - Invalid Witness Reason
- Used by [HDS - Hotspot Discord Status](https://github.com/co8/hds), a Helium Community Tool

---

#### Download HAPpy

Option A: Download from Github

- Download Latest https://github.com/co8/happy/archive/refs/heads/latest.zip

Option B: Clone from Github

```BASH
git clone https://github.com/co8/happy
```

---

#### Use the HAPpy Class

```python
# import happy class from hap.py
from hap import happy

# only required variable. set your hotspot address
hotspot_address = "112MWdscG3DjHTxdCrtuLkkXNSbxCkbqkuiu8X9zFDwsBfa2teCD"

# instantiate happy
happy = happy(hotspot_address)

# response object. newest API data without pagination.
happy.ness
# happy.response is also an alias of happy.ness

print(f"activities count: {len(happy.ness)}")

# output
activities count: 3

# loop through activities in happy.ness
for activity in happy.ness:
  if_reward = ""
  if activity['type'] == "rewards_v2":
    if_reward = f" {activity['hnt_emoji']}{activity['amount']}, {activity['reward_type']}"
  happy_activity = f"{activity['emoji']} {activity['name']}{if_reward} {activity['time_nice']}"
  print(happy_activity)

```

```
# output
🍪 Rewards 🥓0.101, Beacon 21:28 31/AUG
🛸 Valid Witness 21:18 31/AUG
💩 Invalid Witness 20:20 31/AUG
```

sample happy.ness response object

```python
print(happy.ness)
[
    {
        "height": 962925,
        "hash": "2rsmcnn4k7uWbjCCSUu1AbMMRWlyfCp9nGCmX4jjk9A",
        "time": 1629033433,
        "time_nice": "09:17 15/AUG",
        "type": "rewards_v2",
        "subtype": "rewards_beacon",
        "name": "Rewards",
        "emoji": "🍪",
        "hnt_emoji": "🥓",
        "reward_type": "Beacon",
        "amount": "0.101"
    },
    {
        "height": 962925,
        "hash": "ONGyfDAfMQL8gVMPFqUEypxVIjz_l7jxTvG9D2_NkRc",
        "time": 1629033383,
        "time_nice": "09:16 15/AUG",
        "type": "poc_receipts_v1",
        "subtype": "valid_witness",
        "emoji": "🛸",
        "name": "Valid Witness",
        "witnesses": 25,
        "witness_text": "Witnesses",
        "valid_witnesses": 20
    },
    {
        "height": 962925,
        "hash": "xi9XGN8pemkwI0ZKaZEggyxFT5L853yoaaiKoRrcqmc",
        "time": 1629033183,
        "time_nice": "09:13 15/AUG",
        "type": "poc_receipts_v1",
        "subtype": "sent_beacon",
        "name": "Sent Beacon",
        "emoji": "🌋",
        "witnesses": 5,
        "witness_text": "Witnesses",
        "valid_witnesses": 4
    },
    {
        "height": 962925,
        "hash": "aKQx8hY9dJ0RlW6s15DBSmw7Hbs9DNlfi0Dfkgh-BY8",
        "time": 1628985205,
        "time_nice": "19:53 14/AUG",
        "type": "poc_receipts_v1",
        "subtype": "invalid_witness",
        "emoji": "💩",
        "invalid_reason": "RSSI BLB",
        "name": "Invalid Witness",
        "witnesses": 25,
        "witness_text": "Witnesses",
        "valid_witnesses": 24
    }
]
```

You can also pass optional variables to HAPpy

```python
optional_variables = {
    "data": data_list,  # 'data' variable from helium blockchain api response
    "json_file_input": "data.json",  # use a JSON file instead making a Blockchain API request
    "json_file_output": "output.json",  # if activities, output happy.ness response to a JSON file
    "filter": "rewards_v2", # filter by types or subtypes
    "filter": ["rewards_beacon", "rewards_witness"], # 'filter' can be a string or a list
    "cursor": "eyJ0eG4iOiJ6aFh6TWJTQlBLVVpkWVIxRjlIT", # if provided, cursor will be used with API request.
    "get_cursor_and_activities" : True, # if True, API call will get a new cursor and then use it for an API Request. Use 'max' for a shorter response
    "max": 25,  # maximum number of activities. API pagination max is ±100
    "get_hotspot": True, # returns hotspot info to happy.vars["hotspot"]
    "get_wallet": True, # returns wallet info to happy.vars["wallet"]
    "reverse_sort": True,  # reverse sorts response to Ascending Time
    # "get_cursor_only": True, #in_dev # Fetch cursor. no activities
}

#Helium API request using new cursor, maximum of 25 activities, filter by Beacon Rewards, save to output.json
optional_variables = {
    "json_file_output": "output.json",
    "get_cursor_and_activities": True,
    "filter": ["rewards_beacon"],
}

happy = happy(hotspot_address, optional_variables)
print(happy.ness)
# 4 Rewards for Beaconing were found among last 100 activities
#response
[
    {
        "height": 1006532,
        "hash": "3qv_FRfr2urEIZpcbu-tOs9NHzjSxXN3nMcRKaJ0uP8",
        "time": 1631368495,
        "time_nice": "09:54 11/SEP",
        "type": "rewards_v2",
        "subtype": "rewards_beacon",
        "name": "Rewards",
        "emoji": "\ud83c\udf6a",
        "hnt_emoji": "\ud83e\udd53",
        "reward_type": "Beacon",
        "amount": 5278819,
        "amount_nice": "0.053"
    },
    {
        "height": 1005865,
        "hash": "Tpd-4OsWddaPHSuwXElaXGxxUgCxwoYHlayyvh6CpBo",
        "time": 1631327204,
        "time_nice": "22:26 10/SEP",
        "type": "rewards_v2",
        "subtype": "rewards_beacon",
        "name": "Rewards",
        "emoji": "\ud83c\udf6a",
        "hnt_emoji": "\ud83e\udd53",
        "reward_type": "Beacon",
        "amount": 6171442,
        "amount_nice": "0.062"
    },
    {
        "height": 1005362,
        "hash": "n5Ver_vWCyWyQr6xgi2TT8p84vL75cf1BMdT3haK4QM",
        "time": 1631296615,
        "time_nice": "13:56 10/SEP",
        "type": "rewards_v2",
        "subtype": "rewards_beacon",
        "name": "Rewards",
        "emoji": "\ud83c\udf6a",
        "hnt_emoji": "\ud83e\udd53",
        "reward_type": "Beacon",
        "amount": 3270739,
        "amount_nice": "0.033"
    },
    {
        "height": 1003952,
        "hash": "NFhVfIWa8LOuxjmDxFSX5ZYSkBgJlNdB9IxKzj25jFg",
        "time": 1631211785,
        "time_nice": "14:23 09/SEP",
        "type": "rewards_v2",
        "subtype": "rewards_beacon",
        "name": "Rewards",
        "emoji": "\ud83c\udf6a",
        "hnt_emoji": "\ud83e\udd53",
        "reward_type": "Beacon",
        "amount": 3200186,
        "amount_nice": "0.032"
    },
    {
        "height": 1002579,
        "hash": "X4cicC-TWNA06VpWKMYLGgOAYWaMexHhM-LHi6TF5js",
        "time": 1631127000,
        "time_nice": "14:50 08/SEP",
        "type": "rewards_v2",
        "subtype": "rewards_beacon",
        "name": "Rewards",
        "emoji": "\ud83c\udf6a",
        "hnt_emoji": "\ud83e\udd53",
        "reward_type": "Beacon",
        "amount": 3978214,
        "amount_nice": "0.040"
    },
    {
        "height": 1002415,
        "hash": "HkDCBEytl8f8oQNm1Fm4B7z_iTSRTNgWRXOJtqDcOpQ",
        "time": 1631117213,
        "time_nice": "12:06 08/SEP",
        "type": "rewards_v2",
        "subtype": "rewards_beacon",
        "name": "Rewards",
        "emoji": "\ud83c\udf6a",
        "hnt_emoji": "\ud83e\udd53",
        "reward_type": "Beacon",
        "amount": 1665006,
        "amount_nice": "0.017"
    },
    {
        "height": 1002147,
        "hash": "F9FGSQpfkW8sur6bvOOAzUZiChHVR4b2S1uA-pLk-Tw",
        "time": 1631101216,
        "time_nice": "07:40 08/SEP",
        "type": "rewards_v2",
        "subtype": "rewards_beacon",
        "name": "Rewards",
        "emoji": "\ud83c\udf6a",
        "hnt_emoji": "\ud83e\udd53",
        "reward_type": "Beacon",
        "amount": 2832925,
        "amount_nice": "0.028"
    }
]

# No Activities in Response?
# If your response does not have activities, try setting 'get_cursor_and_activities' (optionally 'max') to use API pagination to get recent activities
optional_variables = {
    "get_cursor_and_activities": True
}

```

Pass JSON file as a string or within a dict

```python
# Parse an Blockchain API JSON file, pass as a string
happy = happy(hotspot_address, "activities.json")

# Or pass within a dict with other variables
json_file_input_with_vars = {
  "json_file_input" : "activities.json",
  "max" : 5 # optional
}
happy = happy(hotspot_address, json_file_input_with_vars)
```

<!--
### Other Happy Methods

````python
# values is available in the Vars object

# gets a new page 1 cursor from API
happy.get_cursor()

# happy.vars['cursor']

# gets time as timestamp and nice format
happy.get_time()

# happy.vars['now'] # timestamp
# happy.vars['time'] # 16:24 15/JAN
-->

---

### Access HAPpy Vars

```python
happy = happy(hotspot_address)

print(happy.vars)

{
    "json_file_input": "data.json",
    "json_file_output": "output.json",
    "cursor": "eyJ0eG4iOiJ6aFh6TWJTQlBLVVpkWVIxRjlIT",
    "max": 25,
}

print(happy.hotspot)
"112MWdscG3DjHTxdCrtuLkkXNSbxCkbqkuiu8X9zFDwsBfa2teCD"
```

---

### Access Unparsed Activities from HAPpy

```python
happy = happy(hotspot_address)

print(happy.activities)

[
    {
      "type": "rewards_v2",
      "time": 1629033433,
      "start_epoch": 966367,
      "rewards": [
        {
          "type": "poc_challengees",
          "gateway": "112MWdscG3DjHTxdCrtuLkkXNSbxCkbqkuiu8X9zFDwsBfa2teCD",
          "amount": 10052670,
          "account": "14hriz8pmxm51FGmk1nuijHz6ng9z9McfJZgsg4yxzF2H7No3mH"
        }
      ],
      "height": 966399,
      "hash": "2rsmcnn4k7uWbjCCSUu1AbMMRWlyfCp9nGCmX4jjk9A",
      "end_epoch": 966398
    },
]
```

---

#### Support this Project

Fork this project and submit pull requests

`If you find this project useful please consider supporting it`

HNT: [14hriz8pmxm51FGmk1nuijHz6ng9z9McfJZgsg4yxzF2H7No3mH](https://explorer.helium.com/accounts/14hriz8pmxm51FGmk1nuijHz6ng9z9McfJZgsg4yxzF2H7No3mH)

![](imgs/co8_wallet_qrcode.jpg)

#### Seeking Grants and Bounties

I'm seeking grants and bounties for new projects and to improve and expand this project. [e@co8.com](mailto:e@co8.com)

---

**Check out my other Helium Projects...**

### HDS - Hotspot Discord Status

**Helium Hotspot Activity and Reward Notifications sent to your Discord Channel**

https://github.com/co8/hds

**Listed as a Helium Community Tool** [https://explorer.helium.com/tools](https://explorer.helium.com/tools)

![ACM](imgs/hds-notification.jpg)

---

### ACM - Antenna Cap Mount

**for Rak, Oukeione and Outdoor Fiberglass Dipole Antennas**
**Outdoor or Attic**

https://www.thingiverse.com/thing:4942377

![ACM](imgs/acm-co8.jpg)
