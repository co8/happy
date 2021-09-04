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

####
# Notes:
# To Add: Private methods, functions and data members
# _ : you shouldn’t access this method because it’s not part of the API
# __ : mangle the attribute names of a class to avoid conflicts of attribute names between classes
####

# main class
class happy:
    """HAPpy - Helium API Parser, Python"""

    # attr
    hotspot = ""
    vars = {}
    activities = []  # input
    ness = response = []  # output
    #
    _helium_api_endpoint = "https://api.helium.io/v1/"
    json_file_input = ""  # keep?

    _invalid_reason_short_names = {
        "witness_too_close": "Too Close",
        "witness_rssi_too_high": "RSSI Too High",
        "witness_rssi_below_lower_bound": "RSSI Below Lower Bound",
    }
    __reward_short_names = {
        "poc_witnesses": "Witness",
        "poc_challengees": "Beacon",
        "poc_challengers": "Challenger",
        "data_credits": "Data",
    }

    def load_json_data(self):

        # get json_file_input from vars if exists
        if "json_file_input" in self.vars and bool(self.vars["json_file_input"]):
            self.json_file_input = self.vars["json_file_input"]

        if bool(self.json_file_input):

            with open(self.json_file_input) as json_data_file:
                json_load = json.load(json_data_file)
                self.activities = json_load["data"]
                json_load.pop("data")

                # if more vars after data, load in vars
                if bool(json_load):
                    for key, var in json_load.items():
                        self.vars[key] = var

    def _load_hotspot_data(self):
        if "get_hotspot" in self.vars and bool(self.vars["get_hotspot"]):

            # try to get json or return error
            status = ""
            try:
                # LIVE API data
                hotspot_request = requests.get(
                    self._helium_api_endpoint + "hotspots/" + self.hotspot
                )
                hs = hotspot_request.json()
                hs = hs["data"]

            except requests.RequestException:
                status = "Connectivity"
            except ValueError:  # includes simplejson.decoder.JSONDecodeError
                status = "Parsing JSON"
            except (IndexError, KeyError):
                status = "JSON format"

            if bool(status):
                print(f"Hotspot API Error: {status}")
                quit()

            # success. add vars into vars.hotspot
            else:
                self.vars["hotspot"] = {
                    "address": hs["address"],
                    "owner": hs["owner"],
                    "name": self.nice_hotspot_name(hs["name"]),
                    "initials": "",
                    "status": str(hs["status"]["online"]).upper(),
                    "height": hs["status"]["height"],
                    "block": hs["block"],
                    "reward_scale": "{:.2f}".format(round(hs["reward_scale"], 2)),
                }
                self.vars["hotspot"]["initials"] = self.nice_hotspot_initials(
                    self.vars["hotspot"]["name"]
                )

    # need to get hotspot data to get owner to then get wallet
    def _load_wallet_data(self):

        # get owner from hotspot for request
        if "hotspot" not in self.vars and "owner" not in self.vars["hotspot"]:
            self._load_hotspot_data()

        if "get_wallet" in self.vars and bool(self.vars["get_wallet"]):
            # try to get json or return error
            status = ""
            try:
                # LIVE API data
                wallet_request = requests.get(
                    self._helium_api_endpoint
                    + "accounts/"
                    + self.vars["hotspot"]["owner"]
                )
                w = wallet_request.json()

            except requests.RequestException:
                status = "Connectivity"
            except ValueError:  # includes simplejson.decoder.JSONDecodeError
                status = "Parsing JSON"
            except (IndexError, KeyError):
                status = "JSON format"

            if bool(status):
                print(f"Wallet API Error: {status}")
                quit()

            # success. add vars into vars.wallet
            else:
                self.vars["wallet"] = {
                    "block": w["data"]["block"],
                    "balance": w["data"]["balance"],
                    "balance_nice": self.nice_hnt_amount_or_seconds(
                        w["data"]["balance"]
                    ),
                    "dc_balance": w["data"]["dc_balance"],
                    "dc_balance_nice": self.nice_hnt_amount_or_seconds(
                        w["data"]["dc_balance"]
                    ),
                    "staked_balance": w["data"]["staked_balance"],
                    "staked_balance_nice": self.nice_hnt_amount_or_seconds(
                        w["data"]["staked_balance"]
                    ),
                }

    def trim_activities(self):
        if (
            "max" in self.vars
            and bool(self.vars["max"])
            and len(self.activities) > self.vars["max"]
        ):
            del self.activities[self.vars["max"] :]

    def get_time(self):
        now = datetime.now()
        self.vars["now"] = round(datetime.timestamp(now))
        self.vars["time"] = str(now.strftime("%H:%M %D"))

    def nice_date(self, time):
        timestamp = datetime.fromtimestamp(time)
        return timestamp.strftime("%H:%M %d/%b").upper()

    def nice_hotspot_name(self, name):
        return name.replace("-", " ").upper()

    def nice_hotspot_initials(self, name):
        return "".join(item[0].upper() for item in name.split())

    def nice_hnt_amount_or_seconds(self, amt):
        niceNum = 0.00000001
        niceNumSmall = 100000000

        # float. for time i
        if isinstance(amt, float):
            amt_output = "{:.2f}".format(amt)

        # int. up to 3 decimal payments
        else:
            amt_output = "{:.3f}".format(amt * niceNum)

        # int. 8 decimal places for micropayments
        if amt in range(0, 100000):
            amt_output = "{:.8f}".format(amt / niceNumSmall).rstrip("0")

        return str(amt_output)

    def _nice_invalid_reason(self, ir):
        """invalid reason nice name, or raw reason if not in dict"""
        return (
            self._invalid_reason_short_names[ir]
            if ir in self._invalid_reason_short_names
            else str(ir)
        )

    def _reward_short_name(self, reward_type):
        """activity type name to short name"""
        return (
            self.__reward_short_names[reward_type]
            if reward_type in self.__reward_short_names
            else reward_type.upper()
        )

    def _write_json(self):
        with open(self.vars["json_file_output"], "w") as outfile:
            json.dump(self.ness, outfile)

    def get_cursor(self):
        try:
            # LIVE API data
            activity_endpoint = (
                self._helium_api_endpoint + "hotspots/" + self.hotspot + "/activity/"
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
    def _load_activity_data(self):

        # get activities from "data" in loadvars
        if "data" in self.vars:
            self.activities = self.vars["data"]

        # add cursor if set, get and set cursor if get_cursor_and_activities
        else:
            add_cursor = ""
            if (
                "cursor" in self.vars
                and bool(self.vars["cursor"])
                or "get_cursor_and_activities" in self.vars
                and bool(self.vars["get_cursor_and_activities"])
            ):
                if "get_cursor_and_activities" in self.vars:
                    self.get_cursor()
                elif "cursor" in self.vars and bool(self.vars["cursor"]):
                    add_cursor = f"?cursor={self.vars['cursor']}"
                add_cursor = f"?cursor={self.vars['cursor']}"

            # try to get json or return error
            status = ""
            try:
                # LIVE API data
                activity_endpoint = (
                    self._helium_api_endpoint
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

            self.activities = data["data"]

    ###############################################

    def _loop_activities(self):

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
                        parsed_activity["reward_type"] = self._reward_short_name(
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
                    parsed_activity = self._poc_receipts_v1(activity)

                # other
                else:
                    parsed_activity["type"] = activity["type"]
                    other_type_name = activity["type"]
                    parsed_activity["name"] = other_type_name.upper()
                    parsed_activity["emoji"] = "🚀"

                self.ness.append(parsed_activity)
            self._filter_ness()
            self._clone_ness_response()

    def _clone_ness_response(self):
        """Response is an alias of Ness"""
        self.response = self.ness

    def _filter_ness(self):
        # filtering
        if "filter" in self.vars:
            # if string, convert filter to list
            filters = self.vars["filter"]
            if isinstance(self.vars["filter"], str):
                filters = []
                filters.append(self.vars["filter"])

            # loop and find matches
            self_ness_filtered = []
            for ness_index, ness_var in enumerate(self.ness):
                if (
                    self.ness[ness_index]["type"] in filters
                    or self.ness[ness_index]["subtype"] in filters
                ):
                    self_ness_filtered.append(self.ness[ness_index])

            self.ness = self_ness_filtered  # replace

    def _poc_receipts_v1(self, activity):

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
                        parsed_poc["invalid_reason"] = self._nice_invalid_reason(
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
    def __init__(self, hotspot, loadvars={}):
        """init"""

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
            self._load_activity_data()

        # loop activities
        self._loop_activities()

        # if set in loadvars
        # if load_wallet set in loadvars
        self._load_hotspot_data()

        # if set in loadvars
        self._load_wallet_data()

        if "json_file_output" in self.vars and bool(self.vars["json_file_output"]):
            self._write_json()
