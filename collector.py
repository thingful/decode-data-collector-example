#!/usr/bin/env python

import base64
from datetime import datetime, timedelta
import json

from google.protobuf.timestamp_pb2 import Timestamp
from datastore_client.datastore_pb2_twirp import DatastoreClient
from datastore_client.datastore_pb2 import WriteRequest, ReadRequest
from zenroom import zenroom

client = DatastoreClient('https://datastore.decodeproject.eu')

# create a read request for the policy/community of interest. Note we leave
# `end_time` nil so we are trying to read everything up until "now"
rr = ReadRequest()

# the community id should be passed in by some sort of configuration rather
# than being fixed
rr.community_id = 'f8a8cd8e-61a1-43ae-91dc-a64030925c82'

# set start time to some point in the past (here we use 1 hour ago but could be
# whatever interval the collector requires)
start_time = datetime.utcnow() - timedelta(hours=1)
rr.start_time.FromDatetime(start_time)

# make the first request
resp = client.read_data(rr)

# load the decryption script
with open('decrypt.lua') as file:
    script = file.read()

# create decryption keys - this should be replaced with the private key loaded
# from the environment or other configuration
keys = '{ "community_seckey": "CPzY3PvJXXwl9JVWKyLhpo36xbD3729XBZV3XoTVig8=" }'

# decrypt attempts to decrypt a chunk of data using zenroom, printing out the
# decryted values
def decrypt(ev):
    # execute returns a tuple now - not sure what we should do with the err value
    result, err = zenroom.execute(script.encode(), keys=keys.encode(), data=ev.data, verbosity=1)

    # we decode the returned data and parse the json
    msg = json.loads(result.decode("utf-8"))

    # our actual data packet is passed as another JSON object passed as a field in the main message
    data = json.loads(msg['data'])
    print(data)

# now iterate through all pages of data available for the time interval
while True:
    for ev in resp.events:
        decrypt(ev)

    # if no more results then break the loop
    if resp.next_page_cursor == '':
        break

    # else get the next cursor value and fetch again
    rr.page_cursor = resp.next_page_cursor
    resp = client.read_data(rr)
