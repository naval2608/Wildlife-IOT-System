__author__ = 'naval gupta'

from CoAP_BaseClient import BaseClient;

sensor = BaseClient("4567ABCD",1,'localhost',60001)
sensor.process()