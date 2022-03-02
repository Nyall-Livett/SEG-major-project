import jwt
import requests
import json
from time import time
from datetime import datetime


# API Key and API secret to connect to zoom API
API_KEY = 'bsPNOk1ST0ilGm8imZfL3w'
API_SEC = 'tgaBPU20rystSbPiOdXIoh25m5n0bUvpGMa3'

# function to create a json web token for authorization to access zoom API using pyjwt module
def createjwt():
    # create a token using the api key and the api secret key
	token = jwt.encode(
		{'iss': API_KEY, 'exp': time() + 5000},
		API_SEC,
		algorithm='HS256'
	)
	return token


# function to create json data for post requests
def create_JSON_meeting_data(meetingTitle, startTime, meetingDescription):
    d = {
        "topic" : meetingTitle,
        "start_time" : startTime,
        "agenda" : meetingDescription,
        "duration" : "60",
        "type" : 2,
        "timezone" : "Europe/London",
        "settings": {"host_video": "false",
					 "participant_video": "true",
					 "join_before_host": "true",
					 "mute_upon_entry": "false",
					 "watermark": "true",
					 "audio": "both",
					 "auto_recording": "cloud"
					}
    }
    return d

# function that returns a zoom meeting URL
def getZoomMeetingURL(meetingDetails):
    headers = {'authorization' : 'Bearer ' + createjwt(), 'content-type': 'application/json'}
    r = requests.post(f'https://api.zoom.us/v2/users/me/meetings', headers = headers, data = json.dumps(meetingDetails))
    y = json.loads(r.text)
    return y["join_url"]


# function to convert datetime object to json serializable string accepted as time by zoom API
def convertDateTime(dateTime):
    date = dateTime.strftime("%Y-%m-%d")
    time = dateTime.strftime("%H: %M: %S")
    return date + "T" + time
