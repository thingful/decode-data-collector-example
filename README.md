# data collector

This is an attempt to create a basic barebones python example for reading data
from the encrypted datastore for a given community.

## Requirements

* Python 3.6+ (tested with 3.6.7)
* Linux machine (may work on Mac also but I haven't personally tested running zenroom on OSX)

## Usage

* Create a virtualenv and go inside it (recommended not required)
* Install the dependencies listed in requirements.txt (`pip install -r requirements.txt`)
* Edit collector.py to ensure we have a valid community id (the one included should work for now)
* Edit collector.py to put in the real private key of the community dashboard
* Run: `python collector.py`

This should attempt to read and decrypt all data for the dashboard for the last 24 hours.
