import os
import tempfile
from urllib import parse
from time import gmtime, strftime

import json
import urllib.request
import urllib.parse

WUNDERGROUND_ID = "YOUR_ID" # CHANGE ME
WUNDERGROUND_PWD = "YOUR_PASSWORD"  # CHANGE ME

LACROSSE_ID = "YOUR_LACROSSSE_ID"  # CHANGE ME


def mapWindDirection(direction):
    if direction is None:
        return "0"

    if (direction.lower() == "n"):
        return "0"
    elif (direction.lower() == "nne"):
        return "22.5"
    elif direction.lower() == "ne":
        return "45"
    elif direction.lower() == "ene":
        return "67.5"
    elif direction.lower() == "e":
        return "90"
    elif direction.lower() == "ese":
        return "112.5"
    elif direction.lower() == "se":
        return "135"
    elif direction.lower() == "sse":
        return "157.5"
    elif direction.lower() == "s":
        return "180"
    elif direction.lower() == "ssw":
        return "202.5"
    elif direction.lower() == "sw":
        return "225"
    elif direction.lower() == "wsw":
        return "247.5"
    elif direction.lower() == "w":
        return "270"
    elif direction.lower() == "wnw":
        return "292.5"
    elif direction.lower() == "nw":
        return "315"
    elif direction.lower() == "nnw":
        return "337.5"
    else:
        return "0"


def scrapeLaCrosseData():
    params = {"ID": WUNDERGROUND_ID, "PASSWORD": WUNDERGROUND_PWD, "action": "updateraw"}

    lacrosse_url = 'http://lacrossealertsmobile.com/laxservices/device_info.php?&deviceid=' + LACROSSE_ID

    request = urllib.request.Request(lacrosse_url)
    response = urllib.request.urlopen(request)
    json_obj = json.loads(response.read().decode())

    obs = json_obj['device0']["obs"][0]
    params["tempf"] = obs.get("OutdoorTemp")
    params["humidity"] = obs.get("OutdoorHumid")
    params["dewptf"] = obs.get("DewPoint")
    params["winddir"] = mapWindDirection(obs.get("WindDir"))
    params["windspeedmph"] = obs.get("WindVelocity")
    params["windgustmph"] = obs.get("GustVelocity")
    params["rainin"] = obs.get("Rain1hr")
    params["dailyrainin"] = obs.get("Rain24hr")
    params["baromin"] = obs.get("Pressure")
    params["dateutc"] = strftime("%Y-%m-%d %H:%M:%S", gmtime(obs.get("utctime")))

    return params


def postWundergroundData(params):
    weatherunderground_url = "https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?"
    weatherunderground_url += parse.urlencode(params)

    print(weatherunderground_url)
    request = urllib.request.Request(weatherunderground_url)
    response = urllib.request.urlopen(request)
    print(response.read().decode())


def postData(params):
    file_name = os.path.join(tempfile.gettempdir(), 'last_data.json')
    open(file_name, 'a').close()

    with open(file_name, "r+") as file:
        try:
            previous_sent = json.load(file)
            if params["dateutc"] == previous_sent['dateutc']:
                return False
        except:
            pass

        file.seek(0)
        file.truncate()
        json.dump(params, file)
        return True


params = scrapeLaCrosseData()
if postData(params):
    postWundergroundData(params)
