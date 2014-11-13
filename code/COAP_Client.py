__author__ = 'NAVAL'

import sys
import getopt
import coapy.connection
import coapy.options
import coapy.link

ep = coapy.connection.EndPoint()
ep.socket.bind(('', coapy.COAP_PORT))
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

