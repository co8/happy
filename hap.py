#!/usr/bin/python3

############################
# HAPpy - Helium API Parser, Python
# https://github.com/co8/happy
#
# co8.com
# enrique r grullon
# e@co8.com
# discord: co8#1934
############################

# modules/libraries
from io import StringIO
import sys
import time
import requests
import json
from datetime import datetime

# main class
class happy:
    """HAPpy - Helium API Parser, Python"""

    # attr
    hotspot = json_file_input = ""
    vars = {}
    activities = {}
    output = []
    get_hotspot_data = False

    # vars
    helium_api_endpoint = "https://api.helium.io/v1/"
    hs = {}
    activities = []

    # config_file = "config.json"
    # output_message = []
    # activity_history = []
    # wellness_check = history_repeats = wellness_check_seconds = 0
    # report_interval_seconds = output_message_length = 0
    # interval_pop_status_seconds = int(60 * pop_status_minutes)
    # send = send_report = add_welcome = send_wellness_check = False

    invalid_reason_short_names = {
        "witness_too_close": "Too Close",
        "witness_rssi_too_high": "RSSI Too High",
        "witness_rssi_below_lower_bound": "RSSI BLB",
    }
    reward_short_names = {
        "poc_witnesses": "Witness",
        "poc_challengees": "Beacon",
        "poc_challengers": "Challenger",
        "data_credits": "Data",
    }

    def load_json_data(self):

        # get json_file_input from vars if exists
        if "json_file_input" in self.vars and bool(self.vars["json_file_input"]):
            self.json_file_input = self.vars["json_file_input"]

        # print(self.json_file_input)
        # exit()

        if bool(self.json_file_input):

            with open(self.json_file_input) as json_data_file:
                json_load = json.load(json_data_file)
                self.activities = json_load["data"]
                json_load.pop("data")

                # if more vars after data, load in vars
                if bool(json_load):
                    for key, var in json_load.items():
                        self.vars[key] = var

    def get_time(self):
        # global hs
        # time functions
        now = datetime.now()
        self.vars["now"] = round(datetime.timestamp(now))
        self.vars["time"] = str(now.strftime("%H:%M %D"))

    def nice_date(self, time):
        timestamp = datetime.fromtimestamp(time)
        return timestamp.strftime("%H:%M %d/%b").upper()

    def nice_hotspot_name(name):
        return name.replace("-", " ").upper()
        # if not bool(config["name"]):
        #    config["name"] = name.replace("-", " ").upper()
        # return config["name"]

    def nice_hotspot_initials(name):
        return "".join(item[0].upper() for item in name.split())
        # if not bool(config["initials"]):
        #    name = nice_hotspot_name(name)
        #    config["initials"] = "".join(item[0].upper() for item in name.split())
        # return config["initials"]

    def nice_hnt_amount_or_seconds(self, amt):
        niceNum = 0.00000001
        niceNumSmall = 100000000

        if isinstance(amt, float):
            # float. for time i
            amt_output = "{:.2f}".format(amt)
        else:
            # int. up to 3 decimal payments
            amt_output = "{:.3f}".format(amt * niceNum)

        # int. 8 decimal places for micropayments
        # if amt > 0 and amt < 100000 :
        if amt in range(0, 100000):
            amt_output = "{:.8f}".format(amt / niceNumSmall).rstrip("0")
            # amt_output = f"`{amt_output}`"

        return str(amt_output)

    # invalid reason nice name, or raw reason if not in dict
    def nice_invalid_reason(self, ir):
        return (
            self.invalid_reason_short_names[ir]
            if ir in self.invalid_reason_short_names
            else str(ir)
        )

    # activity type name to short name
    def reward_short_name(self, reward_type):
        return (
            self.reward_short_names[reward_type]
            if reward_type in self.reward_short_names
            else reward_type.upper()
        )

    def write_json(self):
        print(f"writing json: {self.vars['json_file_output']}")
        with open(self.vars["json_file_output"], "w") as outfile:
            json.dump(happy.output, outfile)

    ###############################################
    def load_activity_data(self):
        # global activities, config, hs, wellness_check, send, send_report, send_wellness_check

        # try to get json or return error
        status = ""
        try:
            # LIVE API data
            activity_endpoint = (
                self.helium_api_endpoint + "hotspots/" + self.hotspot + "/activity/"
            )
            activity_request = requests.get(activity_endpoint)
            data = activity_request.json()
            self.activities = data["data"]

            ### DEV Only
            ###LOCAL load data.json
            # with open("data.json") as json_data_file:
            #  data = json.load(json_data_file)

        except requests.RequestException:
            status = "Connectivity"
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            status = "Parsing JSON"
        except (IndexError, KeyError):
            status = "JSON format"

        if bool(status):
            print("Activity API Error: {status}")
            quit()

        # quit if no data
        if not bool(self.activities):
            print("Activity API: No Data")
            quit()

        # no data or send_report false
        # elif not data["data"]:
        #    print("API Success. No activities")
        #    quit()

        # set activities, set last.send, update config
        else:
            # send = True
            self.activities = data["data"]

    ###############################################

    def loop_activities(self):

        if bool(self.activities):
            for activity in self.activities:
                parsed_activity = {}
                # activity time
                parsed_activity["hash"] = activity["hash"]
                parsed_activity["time"] = activity["time"]
                parsed_activity["time_nice"] = self.nice_date(activity["time"])

                # reward
                if activity["type"] == "rewards_v2":
                    for reward in activity["rewards"]:
                        parsed_activity["type"] = activity["type"]
                        parsed_activity["name"] = "Rewards"
                        parsed_activity["emoji"] = "🍪"
                        parsed_activity["hnt_emoji"] = "🥓"
                        parsed_activity["reward_type"] = self.reward_short_name(
                            reward["type"]
                        )
                        parsed_activity["amount"] = self.nice_hnt_amount_or_seconds(
                            reward["amount"]
                        )
                        # output_message.append(f"🍪 Reward 🥓{amt}, {rew}  `{time}`")
                # transferred data
                elif activity["type"] == "state_channel_close_v1":
                    parsed_activity["type"] = activity["type"]
                    parsed_activity["name"] = "Transferred Packets"
                    parsed_activity["emoji"] = "🚛"
                    for summary in activity["state_channel"]["summaries"]:
                        packet_plural = "s" if summary["num_packets"] != 1 else ""
                        parsed_activity["num_packets"] = summary["num_packets"]
                        parsed_activity["packets_text"] = f"Packet{packet_plural}"
                        parsed_activity["num_dcs"] = summary["num_dcs"]

                        # output_message.append(
                        #    f"🚛 Transferred {summary['num_packets']} Packet{packet_plural} ({summary['num_dcs']} DC)  `{time}`"
                        # )

                # ...challenge accepted
                elif activity["type"] == "poc_request_v1":
                    parsed_activity["type"] = activity["type"]
                    parsed_activity["name"] = "Created Challenge..."
                    parsed_activity["emoji"] = "🎲"
                    # output_message.append(f"🎲 Created Challenge...  `{time}`")

                # beacon sent, valid witness, invalid witness
                elif activity["type"] == "poc_receipts_v1":
                    parsed_activity = self.poc_receipts_v1(activity)
                    # parsed_poc = poc_receipts_v1(activity)
                    # parsed_activity = {**parsed_activity, **parsed_poc}

                # other
                else:
                    parsed_activity["type"] = activity["type"]
                    other_type_name = activity["type"]
                    parsed_activity["name"] = other_type_name.upper()
                    parsed_activity["emoji"] = "🚀"
                    # output_message.append(f"🚀 {other_type.upper()}  `{time}`")

                self.output.append(parsed_activity)

    def poc_receipts_v1(self, activity):

        parsed_poc = {}

        # valid_text = "💩  Invalid"
        valid_text = "Invalid"
        # time = nice_date(activity["time"])
        parsed_poc["hash"] = activity["hash"]
        parsed_poc["time"] = activity["time"]
        parsed_poc["time_nice"] = self.nice_date(activity["time"])
        parsed_poc["type"] = "poc_receipts_v1"

        witnesses = {}
        wit_count = 0
        if "path" in activity and "witnesses" in activity["path"][0]:
            witnesses = activity["path"][0]["witnesses"]
            wit_count = len(witnesses)
        # pluralize Witness
        wit_plural = "es" if wit_count != 1 else ""
        wit_text = f"{wit_count} Witness{wit_plural}"

        # challenge accepted
        if "challenger" in activity and activity["challenger"] == self.hotspot:
            # output_message.append(f"🏁 ...Challenged Beaconer, {wit_text}  `{time}`")
            parsed_poc["name"] = "...Challenged Beaconer"
            parsed_poc["witnesses"] = len(witnesses)
            parsed_poc["witness_text"] = f"Witness{wit_plural}"

        # beacon sent
        elif (
            "challengee" in activity["path"][0]
            and activity["path"][0]["challengee"] == self.hotspot
        ):

            # beacon sent plus witness count and valid count
            valid_wit_count = 0
            for wit in witnesses:
                if bool(wit["is_valid"]):
                    valid_wit_count = valid_wit_count + 1
            msg = f"🌋 Sent Beacon, {wit_text}"
            if bool(wit_count):
                if valid_wit_count == len(witnesses):
                    valid_wit_count = "All"
                # msg += f", {valid_wit_count} Valid"
            # msg += f"  `{time}`"
            # output_message.append(msg)

            parsed_poc["name"] = "Sent Beacon"
            parsed_poc["emoji"] = "🌋"
            parsed_poc["witnesses"] = len(witnesses)
            parsed_poc["witness_text"] = f"Witness{wit_plural}"
            parsed_poc["valid_witnesses"] = valid_wit_count

        # witnessed beacon plus valid or invalid and invalid reason
        elif bool(witnesses):
            vw = 0  # valid witnesses
            valid_witness = False
            for w in witnesses:

                # valid witness count among witnesses
                if "is_valid" in w and bool(w["is_valid"]):
                    vw = vw + 1

                if w["gateway"] == self.hotspot:
                    witness_info = ""
                    if bool(w["is_valid"]):
                        valid_witness = True
                        # valid_text = "🛸 Valid"
                        valid_text = "Valid"
                        parsed_poc["emoji"] = "🛸"
                        witness_info = f", 1 of {wit_count}"
                    elif "invalid_reason" in w:
                        # valid_text = "💩 Invalid"
                        valid_text = "Invalid"
                        parsed_poc["emoji"] = "💩"
                        witness_info = ", " + self.nice_invalid_reason(
                            w["invalid_reason"]
                        )

            # add valid witness count among witnesses
            if bool(valid_witness) and vw >= 1:
                vw = "All" if vw == len(witnesses) else vw
                witness_info += f", {vw} Valid"

            parsed_poc["name"] = f"{valid_text} Witness"
            parsed_poc["witnesses"] = wit_count
            parsed_poc["witness_text"] = f"Witness{wit_plural}"
            parsed_poc["valid_witnesses"] = vw

            # output_message.append(f"{valid_text} Witness{witness_info}  `{time}`")

        # other
        else:
            ac_type = activity["type"]
            parsed_poc["name"] = ac_type.upper()
            parsed_poc["emoji"] = "🏁"
            # output_message.append(f"🏁 poc_receipts_v1 - {ac_type.upper()}  `{time}`")

        return parsed_poc

    ##############################
    # init
    def __init__(self, hotspot, loadvars={}):

        if not bool(hotspot):
            print("happy needs a hotspot address to get latest activities")
            quit()
        self.hotspot = hotspot

        # loadvars is str and is ends with .json
        if isinstance(loadvars, str) and loadvars.find(".json") != -1:
            self.vars["json_file_input"] = loadvars
            self.load_json_data()
            print(f"json input str: {self.vars['json_file_input']}")
        elif (
            "json_file_input" in loadvars
            and loadvars["json_file_input"].find(".json") != -1
        ):

            self.json_file_input = loadvars["json_file_input"]
            print(f"vars.json_file_input: {self.json_file_input}")
            # load json, set as activities
            self.load_json_data()

        # loadvars is dict has "data" and bool("data")
        if (
            loadvars
            and isinstance(loadvars, dict)
            and "data" in loadvars
            and bool(loadvars["data"])
        ):
            self.activities = loadvars["data"]
            # print(self.activities)
            loadvars.pop("data")

        # if loadvars dict and more than "data", load into vars
        if isinstance(loadvars, dict) and bool(loadvars):
            if "json_file_input" in self.vars:
                self.json_file_input = loadvars["json_file_input"]
            # load json, set as activities
            self.load_json_data()

            for key, var in loadvars.items():
                self.vars[key] = var

        # load activities if no json file as loadvars as str or as loadvars.json_file_input
        if not bool(self.json_file_input):
            # get live data
            self.load_activity_data()

        # loop activities
        self.loop_activities()

        if "json_file_output" in self.vars and bool(self.vars["json_file_output"]):
            self.write_json()
