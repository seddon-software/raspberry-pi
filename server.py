import cherrypy
import json
import math
import datetime
import logging.handlers
import socket
import announcer
from constants import PORT

def switchOffCheeryPyLogging(cherrypy):
    access_log = cherrypy.log.access_log
    for handler in tuple(access_log.handlers):
        access_log.removeHandler(handler)

data = []
n = 0
raspberryPiData = [0, 0, 0, 0]

class Root(object):
    def sendHeaders(self, **d):
        code = d["code"] if "code" in d else 200
        mimeType = d["mimeType"] if "mimeType" in d else "text/html"
        cherrypy.response.status = code
        cherrypy.response.headers['Content-type'] = mimeType

    def do_POST(self):
        def updateData():
            try:
                device, value = results.split(":")
                raspberryPiData[int(device)] = value
            except:
                print("***", results)

        global raspberryPiData
        contentLength = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(contentLength))
        results = rawbody.decode()
        updateData()
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
                return data
            except:
                self.sendHeaders(code=404)


        fileName, _ = parseInputUrl()
        if(fileName == "data"):
            self.sendHeaders(mimeType="application/json")
            d1 = raspberryPiData[1]
            d2 = raspberryPiData[2]
            d3 = raspberryPiData[3]
            data = {"device1":d1, "device2":d2, "device3":d3, "device4":d3+d2}
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


print("cherrypy server:", socket.gethostbyname(socket.gethostname()))
print("port:", PORT)
print("")
cherrypy.quickstart(Root(), '/')

