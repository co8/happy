# HAPpy - Helium API Parser, Python

### Easily Access Helium Blockchain API Data with just your Hotspot Address

<!-- **Listed as a Helium Community Tool** [https://explorer.helium.com/tools](https://explorer.helium.com/tools) -->

```PYTHON
# only need your hotspot address
hotspot_address = "112MWdscG3DjHTxdCrtuLkkXNSbxCkbq..."

happy = happy(hotspot_address)

#Response
print(happy.ness)

{
    "height": 966398,
    "hash": "ONGyfDAfMQL8gVMPFqUEypxVIjz_l7jxTvG9D2_NkRc",
    "time": 1629033383,
    "time_nice": "09:16 15/AUG",
    "type": "poc_receipts_v1",
    "emoji": "🛸",
    "name": "Valid Witness",
    "witnesses": 25,
    "witness_text": "Witnesses",
    "valid_witnesses": 20
},
```

🛸 Valid Witness, 1 of 25, 20 Valid, 09:16 15/AUG at height 966,398

---

#### Features

- Uses [Helium Blockchain API](https://docs.helium.com/api/blockchain/introduction/)
- Python 3.9+
- Easy to use Response
- Optionally Write Response to JSON file
- Parsed and Formatted Data
  - Name of Activity Type
  - Reward Amounts and Types
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

- Download Latest https://github.com/co8/happy/archive/refs/heads/master.zip

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
hotspot_address = "112MWdscG3DjHTxdCrtuLkkXNSbxCkbq..."

#instantiate happy
happy = happy(hotspot_address)

#response object. newest API data without pagination
happy.ness


print(f"activities count: {len(happy.ness)}")
#activities count: 3

#loop through activities in happy.ness
for activity in happy.ness:
    happy_activity = f"{activity['emoji']} {activity['name']} {activity['time_nice']}"
  if activity['type'] == "rewards_v2":
    happy_activity .= f", {activity['hnt_emoji']} {activity['amount']}"
  print(happy_activity)

```

```
#output
🍪 Rewards 21:28 31/AUG, 🥓0.101
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
        "emoji": "💩",
        "invalid_reason": "RSSI BLB",
        "name": "Invalid Witness",
        "witnesses": 25,
        "witness_text": "Witnesses",
        "valid_witnesses": 24
    }
]
```

You can also pass optional attributes to HAPpy

```python
optional_attributes = {
    "json_file_input": "data.json",  # use a JSON file instead making an Blockchain API call
    "json_file_output": "output.json",  # if activities, output happy.ness response to a JSON file
    "get_cursor": False,  # if True, API call will get a new cursor and use it for an API Request
    "cursor": "eyJ0eG4iOiJ6aFh6TWJTQlBLVVpkWVIxRjlIT...", # provide cursor for API pagination.
    "max": 25,  # limit number of activities to parse. API pagination max is ±100
}

#limit of 25 activities, save to output.json
optional_attributes = {
    "json_file_output": "output.json",
    "get_cursor": True
    "max": 25,
}

# No Activities in Response?
# If your response does not have activities, try setting 'get_cursor' and 'max' to use API pagination to get recent activities

happy = happy(hotspot_address, optional_attributes)

```

Pass JSON file as a string or within a dict

```python
# Parse an Blockchain API JSON file, pass as a string
happy = happy(hotspot_address, "activities.json")

#Or pass within a dict with other attributes
json_file_input_with_vars = {
  "json_file_input" : "activities.json",
  "max" : 5 # optional
}
happy = happy(hotspot_address, json_file_input_with_vars)
```

---

### Access HAPpy Vars

```python
happy = happy(hotspot_address)

print(happy.vars)

{
    "json_file_input": "data.json",
    "json_file_output": "output.json",
    "get_cursor": False,
    "cursor": "eyJ0eG4iOiJ6aFh6TWJTQlBLVVpkWVIxRjlIT...",
    "max": 25,
}
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
