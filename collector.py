#!/usr/bin/env python

import base64
from datetime import datetime, timedelta

from google.protobuf.timestamp_pb2 import Timestamp
from datastore_client.datastore_pb2_twirp import DatastoreClient
from datastore_client.datastore_pb2 import WriteRequest, ReadRequest

client = DatastoreClient('https://datastore.decodeproject.eu')

# create a read request for the policy/community of interest. Note we leave
# `end_time` nil so we are trying to read everything up until "now"
rr = ReadRequest()

# the community id should be passed in by some sort of configuration rather
# than being fixed
rr.community_id = '22ba20bf-4675-4d3a-9bcf-612b7db7a267'

# set start time to some point in the past (here we use 1 day ago but could be
# whatever interval the collector requires)
start_time = datetime.now() - timedelta(days=1)
rr.start_time.FromDatetime(start_time)

# make the first request
resp = client.read_data(rr)

# load the decryption script
with open('decrypt.lua') as file:
    script = file.read()

# create decryption keys - this should be replaced with the private key Rohit is using
keys = '{ "community_seckey": "D19GsDTGjLBX23J281SNpXWUdu+oL6hdAJ0Zh6IrRHA=" }'

# decrypt attempts to decrypt a chunk of data using zenroom, printing out the
# decryted values
def decrypt(data):
    result = zenroom.execute(script.encode(), keys=keys.encode(), data=data.encode(), verbosity=1)
    print(result.decode('ascii'))

# now iterate through all pages of data available for the time interval
while True:
    for ev in resp.events:
        #print(ev.event_time.ToJsonString())
        decrypt(ev.data)

    # if no more results then break the loop
    if resp.next_page_cursor == '':
        break

    # else get the next cursor value and fetch again
    rr.page_cursor = resp.next_page_cursor
    resp = client.read_data(rr)
