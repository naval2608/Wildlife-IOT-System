__author__ = 'NAVAL'

import sys
import coapy.connection
import coapy.options
import coapy.link
import time

host = 'localhost'
port = 61616
remote = (host, port)
req = coapy.connection.Message(code=coapy.GET, uri_path="GeoLocation")
ep = coapy.connection.EndPoint()
tx_rec = ep.send(req, remote)
