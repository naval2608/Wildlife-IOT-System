# Demonstration local server.
# In one window:
#  python server.py
# In another window:
#  python coapget.py -h localhost -v
#  python coapget.py -h localhost -u uptime
#  python coapget.py -h localhost -u counter
#  python coapget.py -h localhost -u unknown

import sys
import coapy.connection
import coapy.options
import coapy.link
import time

ep = coapy.connection.EndPoint()
ep.socket.bind(('', coapy.COAP_PORT))

class CounterService (coapy.link.LinkValue):
    __counter = 0

    def process (self, rx_record):
        ctr = self.__counter
        self.__counter += 1
        msg = coapy.connection.Message(coapy.connection.Message.ACK, code=coapy.OK, payload='%d' % (ctr,))
        rx_record.ack(msg)

class UptimeService (coapy.link.LinkValue):
    __started = time.time()

    def process (self, rx_record):
        uptime = time.time() - self.__started
        msg = coapy.connection.Message(coapy.connection.Message.ACK, code=coapy.OK, payload='%g' % (uptime,))
        rx_record.ack(msg)

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

services = ResourceService()
services.add_service(CounterService('counter'))
services.add_service(UptimeService('uptime'))

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
    if uri is None:
        continue
    service = services.lookup(uri.value)
    print 'Lookup %s got %s' % (uri, service)
    if service is None:
        rxr.reset()
        continue
    service.process(rxr)
