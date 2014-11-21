"""
Peter Kutschera, 2013-09-11
Time-stamp: "2014-05-21 12:32:20 peter"

The server gets an ICMM worldstate URL and calculates an indicator

Execution example (Change service part):
https://pinguin2.ait.ac.at/~peter/indicators/pywps.cgi?service=WPS&request=Execute&version=1.0.0&identifier=OverallTime&datainputs=ICMMworldstateURL=http://crisma.cismet.de/pilotE/icmm_api/CRISMA.worldstates/1

"""

"""
    Copyright (C) 2014  AIT / Austrian Institute of Technology
    http://www.ait.ac.at
 
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 2 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
 
    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see http://www.gnu.org/licenses/gpl-2.0.html
"""


#from pywps.Process import WPSProcess                                
#from sys import stderr
import json
import requests
import string
#import urllib
#import time
import datetime
import dateutil.parser
import logging

from Indicator import Indicator
import ICMMtools as ICMM

class Process(Indicator):
    def __init__(self):
        # init process
        Indicator.__init__(
            self,
            identifier="OverallTime", #the same as the file name
            version = "1.0",
            title="Overall time",
            abstract="Incident to last transport")

    def calculateIndicator(self):
        # calculate indicator value
        self.status.set("Start collecting input data", 20)

        jsonData = ICMM.getCaptureData (self.ICMMworldstate)
        # logging.info (jsonData)

        t1 = dateutil.parser.parse (jsonData['incidentTime'])
        # logging.info ("t1: " +  t1.isoformat())
        t2 = t1

        for p in jsonData['patients']:
            if 'transportation_timestamp' in p:
                if p['transportation_timestamp'] is not None:
                    # t = dateutil.parser.parse (p['transportation_timestamp']) # problem: t does not contain time zone !!
                    ts = p['transportation_timestamp']
                    if (len(ts) == 16):
                        ts = ts + ":00.0Z"
                    t = dateutil.parser.parse (ts)
                    # logging.info ("t:  " +  t.isoformat())
                    if t > t2:
                        t2 = t
        # logging.info ("t2: " +  t2.isoformat())

        # create indicator value structure
        indicatorData = {
            'id': self.identifier,
            'name': self.title,
            'description': self.abstract,
            "worldstateDescription": self.worldstateDescription,
            "worldstates":[self.ICMMworldstate.id],
            "type":"timeintervals",
            "data": {
                "intervals": [
                    {
                        "startTime": t1.isoformat(),
                        "endTime": t2.isoformat()
                        }
                    ],
                "color": "#00cc00",
                "linewidth": 2
                }
            }
        return indicatorData


