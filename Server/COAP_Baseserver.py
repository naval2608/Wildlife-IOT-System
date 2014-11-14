import sys
import getopt
import coapy.connection
import coapy.options
import coapy.link
import json

class BaseServer():

    def __init__(self):
        self.host = 'localhost'
        self.port = 61616
        self.uri_path = 'Geolocation'


    def getClientLocation(self):
        remote = (self.host, self.port)
        req = coapy.connection.Message(transaction_type=1,code=coapy.GET, uri_path=self.uri_path)
        ep = coapy.connection.EndPoint()
        tx_rec = ep.send(req, remote)

        while tx_rec.response is None:
            rv = ep.process(1000)
            if rv is None:
                print 'No message received; waiting'
                continue
            msg = rv.message
            print msg

            if msg.RST == tx_rec.response_type:
                print 'Server responded with reset'
                return -1
            if coapy.OK != msg.code:
                print 'Pertinent response code not OK: %d (%s)' % (msg.code, coapy.codes.get(msg.code, 'UNDEFINED'))
                return -1

            ct = msg.findOption(coapy.options.ContentType)
            if (ct is None) or (ct.value_as_string.startswith('text/')):
                print msg.payload
            elif 'application/link-format' == ct.value_as_string:
                data = json.loads(msg.payload)
                print "Got NON Payload from Sensor"
                return data
            else:
                print 'Unhandled content type'
        return 0

