import cherrypy
import json
from cherrypy.process.plugins import Daemonizer

import datetime
import ssl
import sys
import random
import hashlib
import string
from functools import partial
import urllib.parse
import uuid
import re
import logging.handlers


def switchOffCheeryPyLogging(cherrypy):
    access_log = cherrypy.log.access_log
    for handler in tuple(access_log.handlers):
        access_log.removeHandler(handler)

class Root(object):
        
    def sendHeaders(self, **d):
        code = d["code"] if "code" in d else 200
        mimeType = d["mimeType"] if "mimeType" in d else "html/text"
        cherrypy.response.status = code
        cherrypy.response.headers['Content-type'] = mimeType

    def do_POST(self):
        contentLength = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(contentLength))
#         jsonAsString = rawbody.decode("UTF-8")
#         results = json.loads(jsonAsString)
        results = rawbody.decode()
        print(results)
        self.sendHeaders()
        return

    def do_GET(self, args, kwargs):
        pass

    @cherrypy.expose
    def default(self, *args, **kwargs):
        method = cherrypy.request.method
        if method == "GET": 
            return self.do_GET(args, kwargs)
        if method == "POST": 
            self.do_POST()

PORT = 5559
SERVER = "0.0.0.0"

# d = Daemonizer(cherrypy.engine)
# d.subscribe()
cherrypy.config.update(
    { 'server.socket_port': PORT,
      'engine.autoreload.on' : False,
      'environment': 'embedded',
      'server.socket_host': SERVER,
    } )


def setupLogging():
    LOG_FILENAME = "log"

    # Set up a specific logger with our desired output level
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.DEBUG)
    
    # Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1000000, backupCount=10)
    my_logger.addHandler(handler)
    return my_logger



switchOffCheeryPyLogging(cherrypy)
my_logger = setupLogging()
my_logger.debug("server started at {}".format(datetime.datetime.now()))


print("cherrypy server:", SERVER)
print("port:", PORT)
print("")
cherrypy.quickstart(Root(), '/')

