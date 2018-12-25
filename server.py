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
#     for handler in tuple(access_log.handlers):
#         access_log.removeHandler(handler)

data = []
n = 0

class Root(object):
    def sendHeaders(self, **d):
        code = d["code"] if "code" in d else 200
        mimeType = d["mimeType"] if "mimeType" in d else "text/html"
        cherrypy.response.status = code
        cherrypy.response.headers['Content-type'] = mimeType

    def do_POST(self):
        contentLength = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(contentLength))
#         jsonAsString = rawbody.decode("UTF-8")
#         results = json.loads(jsonAsString)
        results = rawbody.decode()
#        print(results)
        data.append()
        self.sendHeaders()
        return

    def do_GET(self, args, kwargs):
        def getMimeType():
            extension = fileName.split(".")[-1]
            if(extension == "ico"): return "image/x-icon"
            if(extension == "css"): return "text/css"
            if(extension == "jpg"): return "image/jpeg"
            if(extension == "png"): return "image/png"
            if(extension == "svg"): return "image/svg+xml"
            return "text/html"

        def parseInputUrl():
            fileName = "/".join(args)
            
            # make graph.html the default pages
            if fileName == "": fileName = "graph.html"            
            queryDictionary = kwargs
            return fileName, queryDictionary

        def doSendRegularFiles(fileName):
            try:
                mimeType = getMimeType()
                self.sendHeaders(mimeType=mimeType)
                f = open(fileName, "r", encoding="UTF-8")
                data = f.read()
                return data  #.encode("UTF-8")
            except:
                self.sendHeaders(code=404)


        fileName, _ = parseInputUrl()
        if(fileName == "data"):
            self.sendHeaders(mimeType="application/json")
            global n
            if n == 10:
                n = -10
            else:
                n += 1
            data = {"device1":n/10}
            data = json.dumps(data)
            return data
        else:                                           
            return doSendRegularFiles(fileName)

    @cherrypy.expose
    def default(self, *args, **kwargs):
        method = cherrypy.request.method
        if method == "GET": 
            z = self.do_GET(args, kwargs)
            return z.encode()
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
      'tools.sessions.on': True,
      'tools.encode.on': True,
      'tools.encode.encoding': 'utf-8',
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

