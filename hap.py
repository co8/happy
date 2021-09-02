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
    activities = {}  # input
    ness = []  # output

    # vars
    helium_api_endpoint = "https://api.helium.io/v1/"
    # hs = {}
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
        "witness_rssi_below_lower_bound": "RSSI Below Lower Bound",
    }
    reward_short_names = {
        "poc_witnesses": "Witness",
        "poc_challengees": "Beacon",
        "poc_challengers": "Challenger",
        "data_credits": "Data",
    }

    def load_json_data(self):
        # print("load_json_data()")
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

    def trim_activities(self):
        if (
            "max" in self.vars
            and bool(self.vars["max"])
            and len(self.activities) > self.vars["max"]
        ):
            # print(f"trim_activities(): {self.vars['max']}")
            del self.activities[self.vars["max"] :]

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
        # print(f"writing json: {self.vars['json_file_output']}")
        with open(self.vars["json_file_output"], "w") as outfile:
            json.dump(self.ness, outfile)

    def get_cursor(self):
        try:
            # LIVE API data
            activity_endpoint = (
                self.helium_api_endpoint + "hotspots/" + self.hotspot + "/activity/"
            )
            activity_request = requests.get(activity_endpoint)
            data = activity_request.json()
            self.vars["cursor"] = data["cursor"]

        except:
            print("cannot get cursor from Helium API. I quit")
            quit()

    # def func_get_cursor_and_activities(self):
    #    if "get_cursor_and_activities" in self.vars:
    #        self.only_get_cursoronly_get_cursor()

    ###############################################
    def load_activity_data(self):
        # global activities, config, hs, wellness_check, send, send_report, send_wellness_check

        # get activities from "data" in loadvars
        if "data" in self.vars:  # and isinstance(self.vars["data"], list):
            self.activities = self.vars["data"]
            # load json, set as activities
            # self.load_json_data()
            # print("data from loadvars ln 180")

        else:

            # add cursor if set, get and set cursor if get_cursor_and_activities
            add_cursor = ""
            if (
                "cursor" in self.vars
                and bool(self.vars["cursor"])
                or "get_cursor_and_activities" in self.vars
                and bool(self.vars["get_cursor_and_activities"])
            ):
                if "get_cursor_and_activities" in self.vars:
                    self.get_cursor()
                    # print("cursor: NEW")
                elif "cursor" in self.vars and bool(self.vars["cursor"]):
                    add_cursor = f"?cursor={self.vars['cursor']}"
                    # print("cursor: existing")
                add_cursor = f"?cursor={self.vars['cursor']}"

            # try to get json or return error
            status = ""
            try:
                # LIVE API data
                activity_endpoint = (
                    self.helium_api_endpoint
                    + "hotspots/"
                    + self.hotspot
                    + "/activity/"
                    + add_cursor
                )
                activity_request = requests.get(activity_endpoint)
                data = activity_request.json()
                self.activities = data["data"]

            except requests.RequestException:
                status = "Connectivity"
            except ValueError:  # includes simplejson.decoder.JSONDecodeError
                status = "Parsing JSON"
            except (IndexError, KeyError):
                status = "JSON format"

            if bool(status):
                print(f"Activity API Error: {status}")
                quit()

            # quit if no data
            # if not bool(self.activities):
            #    resp = "No Activities"
            #    print(resp)
            #    self.vars["response"] = resp
            #    quit()

            # no data or send_report false
            # elif not data["data"]:
            #    print("API Success. No activities")
            #    quit()

            # set activities, set last.send, update config
            # else:
            # send = True
            self.activities = data["data"]

    ###############################################

    def loop_activities(self):

        self.trim_activities()

        if bool(self.activities):
            for activity in self.activities:
                parsed_activity = {}
                # activity time
                parsed_activity["height"] = activity["height"]
                parsed_activity["hash"] = activity["hash"]
                parsed_activity["time"] = activity["time"]
                parsed_activity["time_nice"] = self.nice_date(activity["time"])

                # reward
                if activity["type"] == "rewards_v2":
                    for reward in activity["rewards"]:
                        parsed_activity["type"] = activity["type"]
                        parsed_activity["subtype"] = "rewards"
                        parsed_activity["name"] = "Rewards"
                        parsed_activity["emoji"] = "🍪"
                        parsed_activity["hnt_emoji"] = "🥓"
                        parsed_activity["reward_type"] = self.reward_short_name(
                            reward["type"]
                        )
                        parsed_activity["subtype"] += (
                            "_" + parsed_activity["reward_type"].lower()
                        )
                        parsed_activity["amount"] = self.nice_hnt_amount_or_seconds(
                            reward["amount"]
                        )

                # transferred packets
                elif activity["type"] == "state_channel_close_v1":
                    parsed_activity["type"] = activity["type"]
                    parsed_activity["subtype"] = "packets"
                    parsed_activity["name"] = "Transferred Packets"
                    parsed_activity["emoji"] = "🚛"
                    for summary in activity["state_channel"]["summaries"]:
                        packet_plural = "s" if summary["num_packets"] != 1 else ""
                        parsed_activity["num_packets"] = summary["num_packets"]
                        parsed_activity["packets_text"] = f"Packet{packet_plural}"
                        parsed_activity["num_dcs"] = summary["num_dcs"]

                # ...challenge accepted
                elif activity["type"] == "poc_request_v1":
                    parsed_activity["type"] = activity["type"]
                    parsed_activity["name"] = "Created Challenge..."
                    parsed_activity["subtype"] = "created_challenge"
                    parsed_activity["emoji"] = "🎲"

                # beacon sent, valid witness, invalid witness
                elif activity["type"] == "poc_receipts_v1":
                    parsed_activity = self.poc_receipts_v1(activity)

                # other
                else:
                    parsed_activity["type"] = activity["type"]
                    other_type_name = activity["type"]
                    parsed_activity["name"] = other_type_name.upper()
                    parsed_activity["emoji"] = "🚀"
                    # output_message.append(f"🚀 {other_type.upper()}  `{time}`")

                self.ness.append(parsed_activity)
            self.filter_ness()

    def filter_ness(self):
        # filtering
        if "filter" in self.vars:
            print("filter in vars")
            # if string, convert filter to list
            filters = self.vars["filter"]
            if isinstance(self.vars["filter"], str):
                filters = []
                filters.append(self.vars["filter"])

            print("filters: ", end="")
            print(filters)
            print(type(filters))

            # loop and find matches
            print(f"original count: {len(self.ness)}")
            self_ness_filtered = []
            for ness_index, ness_var in enumerate(self.ness):
                if (
                    self.ness[ness_index]["type"] in filters
                    or self.ness[ness_index]["subtype"] in filters
                ):
                    self_ness_filtered.append(self.ness[ness_index])

            self.ness = self_ness_filtered  # replace
            # print(f"filtered count: {len(self.ness)}")

    def poc_receipts_v1(self, activity):

        parsed_poc = {}
        valid_text = "Invalid"
        parsed_poc["height"] = activity["height"]
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
            parsed_poc["name"] = "...Challenged Beaconer"
            parsed_poc["subtype"] = "challenged_beaconer"
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
            if bool(wit_count):
                if valid_wit_count == len(witnesses):
                    valid_wit_count = "All"

            parsed_poc["name"] = "Sent Beacon"
            parsed_poc["subtype"] = "sent_beacon"
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
                        valid_text = "Valid"
                        parsed_poc["emoji"] = "🛸"
                        witness_info = f", 1 of {wit_count}"
                    elif "invalid_reason" in w:
                        # valid_text = "💩 Invalid"
                        valid_text = "Invalid"
                        parsed_poc["emoji"] = "💩"
                        parsed_poc["invalid_reason"] = self.nice_invalid_reason(
                            w["invalid_reason"]
                        )
                parsed_poc["subtype"] = f"{valid_text.lower()}_witness"

            # add valid witness count among witnesses
            if bool(valid_witness) and vw >= 1:
                vw = "All" if vw == len(witnesses) else vw
                witness_info += f", {vw} Valid"

            parsed_poc["name"] = f"{valid_text} Witness"
            parsed_poc["witnesses"] = wit_count
            parsed_poc["witness_text"] = f"Witness{wit_plural}"
            parsed_poc["valid_witnesses"] = vw

        # other
        else:
            ac_type = activity["type"]
            parsed_poc["name"] = ac_type.upper()
            parsed_poc["emoji"] = "🏁"

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
        elif (
            "json_file_input" in loadvars
            and loadvars["json_file_input"].find(".json") != -1
        ):

            self.json_file_input = loadvars["json_file_input"]
            self.load_json_data()

        # loadvars is dict has "data" and bool("data")
        if (
            loadvars
            and isinstance(loadvars, dict)
            and "data" in loadvars
            and bool(loadvars["data"])
        ):
            self.activities = loadvars["data"]
            loadvars.pop("data")

        # if loadvars dict and more than "data", load into vars
        if isinstance(loadvars, dict) and bool(loadvars):

            # get activities from json file provided in "json_file_input" in loadvars
            if (
                "json_file_input" in self.vars
                and self.vars["json_file_input"].find(".json") != -1
            ):
                self.json_file_input = loadvars["json_file_input"]

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
