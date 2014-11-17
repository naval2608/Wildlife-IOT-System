__author__ = 'naval gupta'

from CoAP_BaseClient import BaseClient;

sensor = BaseClient("1234ABCD",0,'localhost',60002)
sensor.process()
