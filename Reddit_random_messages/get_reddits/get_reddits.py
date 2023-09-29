"""
This script gets reddits titles from the reddit api 
and serve in the first step of the dockerized pipeline.
TODO: add Mongodb connection with pymongo and insert reddits into Mongodb 
"""


import requests
from requests.auth import HTTPBasicAuth
import sys
from config import tokens
from  pprint import pprint

import pymongo

client = pymongo.MongoClient(host="mongodb", port=27017)
db = client.reddit

sys.stdout.reconfigure(encoding='utf-8') # Useful windows user

## PREPARE AUTHENTICATION INFORMATION ##
## FOR REQUESTING A TEMPORARY ACCESS TOKEN ##

basic_auth = HTTPBasicAuth(
    username=tokens['client_id'],
    password=tokens['secret']
)

print(basic_auth)

GRANT_INFORMATION = dict(
    grant_type="password",
    username=tokens['username'], # REDDIT USERNAME
    password=tokens['password'] # REDDIT PASSWORD
)

headers = {
    'User-Agent': "Mozilla"  # header for the request
}

### POST REQUEST FOR ACCESS TOKEN

POST_URL = "https://www.reddit.com/api/v1/access_token"

access_post_response = requests.post(
    url=POST_URL,
    headers=headers,
    data=GRANT_INFORMATION,
    auth=basic_auth
).json()

# Print the Bearer Token sent by the API
print(access_post_response)

### ADDING TO HEADERS THE Authorization KEY

headers['Authorization'] = access_post_response['token_type'] + ' ' + access_post_response['access_token']

print(headers)

## Send a get request to download most popular (hot) Python subreddits title using the new headers.

topic = 'queer'
URL = f"https://oauth.reddit.com/r/{topic}/hot"

response = requests.get(
    url=URL,
    headers=headers
).json()

print(response)

full_response = response['data']['children']

# Go through the full response and define a mongo_input dict
# filled with reddit title and corresponding id

for post in full_response:
    _id = post['data']['id']
    title = post['data']['title']
    mongo_input = {"_id":_id, 'text': title}
    db.posts.insert_one(dict(mongo_input))
    print(mongo_input)



