# Demonstration local server.
# In one window:
#  python server.py
# In another window:
#  python coap_sensor.py -h localhost -u Geolocation

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
                print 'No activity'
                continue
            print rxr.message
            msg = rxr.message
            if coapy.GET != msg.code:
                continue
            uri = msg.findOption(coapy.options.UriPath)
            print "Recieved the URI:",uri
            if uri is None:
                continue
            service = services.lookup(uri.value)
            print 'Lookup %s got %s' % (uri, service)
            if service is None:
                rxr.reset()
                continue
            service.process(rxr)


    def sendGeoLocation(self,rx_record):
       try:
            msg = coapy.connection.Message(coapy.connection.Message.NON,code=coapy.OK, content_type='application/link-format')
            data = {}
            location = {}
            data["rfid"] = "ABCD1234"
            location["latitude"] = 83.21
            location["longitude"] = -45.22
            data["location"] = location
            data["record_time"] = time.time()
            print data
            msg.payload = json.dumps(data)
            ep.send(msg, rx_record.remote)
            print "Sending GeoLocation Details as NON Message."
        except Exception as error:
            print "Error: {err}".format(err=error)


class GeolocationService (coapy.link.LinkValue):

    def process (self, rx_record):
        try:
            msg = coapy.connection.Message(coapy.connection.Message.NON,code=coapy.OK, content_type='application/link-format')
            data = {}
            location = {}
            data["rfid"] = "ABCD1234"
            location["latitude"] = 83.21
            location["longitude"] = -45.22
            data["location"] = location
            data["record_time"] = time.time()
            print data
            msg.payload = json.dumps(data)
            ep.send(msg, rx_record.remote)
            print "Sending GeoLocation Details as NON Message."
        except Exception as error:
            print "Error: {err}".format(err=error)

class ResourceService (coapy.link.LinkValue):

    __services = None

    def __init__ (self, *args, **kw):
        super(ResourceService, self).__init__('.well-known/r', ct=[coapy.media_types_rev.get('application/link-format')])
        self.__services = { self.uri : self }

    def add_service (self, service):
        self.__services[service.uri] = service
        
    def lookup (self, uri):
        return self.__services.get(uri)

    def process (self, rx_record):
        msg = coapy.connection.Message(coapy.connection.Message.ACK, code=coapy.OK, content_type='application/link-format')
        msg.payload = ",".join([ _s.encode() for _s in self.__services.itervalues() ])
        rx_record.ack(msg)

ep = coapy.connection.EndPoint()
ep.socket.bind(('', coapy.COAP_PORT))
services = ResourceService()
services.add_service(GeolocationService('Geolocation'))
while True:
    rxr = ep.process(10000)
    if rxr is None:
        print 'No activity'
        continue
    print rxr.message
    msg = rxr.message
    if coapy.GET != msg.code:
        continue
    uri = msg.findOption(coapy.options.UriPath)
    print "Recieved the URI:",uri
    if uri is None:
        continue
    service = services.lookup(uri.value)
    print 'Lookup %s got %s' % (uri, service)
    if service is None:
        rxr.reset()
        continue
    service.process(rxr)
