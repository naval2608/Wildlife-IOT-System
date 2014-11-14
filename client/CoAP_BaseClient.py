__author__ = 'naval gupta'

import sys
import coapy.connection
import coapy.options
import coapy.link
import time
import json
import datetime

class BaseClient():
    def __init__(self):
        self.ep = coapy.connection.EndPoint()
        self.ep.socket.bind(('', coapy.COAP_PORT))

    def process(self):
        while True:
            rxr = self.ep.process(10000)
            if rxr is None:
                print 'No Request'
                continue
            print rxr.message
            msg = rxr.message
            if coapy.GET != msg.code:
                continue
            uri = msg.findOption(coapy.options.UriPath)
            print "Recieved the GET URI:",uri
            if uri is None:
                continue
            if uri.value == "Geolocation":
                self.sendGeoLocation(rxr)
            else:
                rxr.reset()
                continue

    def sendGeoLocation(self,rx_record):
        try:
            msg = coapy.connection.Message(coapy.connection.Message.NON,code=coapy.OK, content_type='application/link-format')
            data = self.generateGeoLocation()
            msg.payload = json.dumps(data)
            self.ep.send(msg, rx_record.remote)
            print "Sending GeoLocation Details as NON Message."
        except Exception as error:
            print "Error: {err}".format(err=error)

    def generateGeoLocation(self):
        data = {}
        location = {}
        data["rfid"] = "ABCD1234"
        location["latitude"] = 83.21
        location["longitude"] = -45.22
        data["location"] = location
        data["record_time"] = time.time()
        return data