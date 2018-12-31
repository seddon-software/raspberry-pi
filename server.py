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
raspberryPiData = None
raspberryPiInfo = None
numberOfDevices = None

class Root(object):
    def sendHeaders(self, **d):
        code = d["code"] if "code" in d else 200
        mimeType = d["mimeType"] if "mimeType" in d else "text/html"
        cherrypy.response.status = code
        cherrypy.response.headers['Content-type'] = mimeType

    def do_POST(self, args, kwargs):
        def setupDataStructures():
            global raspberryPiData
            global raspberryPiInfo
            global numberOfDevices
            numberOfDevices = len(results)
            raspberryPiData = [0.0] * (numberOfDevices+1)
            raspberryPiInfo = results

        def updateData():
            global raspberryPiData
            global raspberryPiInfo
            try:
                device, value = results.split(":")
                raspberryPiData[int(device)] = value
            except:
                print("***", results)

        if args:
            fileName = args[0]
        else:
            fileName = ""
        contentLength = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(contentLength))
        results = rawbody.decode()

        if fileName == "init":
            print(results)
            setupDataStructures()
        else:
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
        if(fileName == "init"):
            self.sendHeaders(mimeType="application/json")
            data = json.dumps(raspberryPiInfo)
            return data
        elif(fileName == "data"):
            self.sendHeaders(mimeType="application/json")
            data = {}
            for n in range(1, numberOfDevices):
                data[f"device{n}"] = raspberryPiData[n]
#                 d1 = raspberryPiData[1]
#                 d2 = raspberryPiData[2]
#                 d3 = raspberryPiData[3]
#                 d4 = raspberryPiData[4]
#                 d5 = raspberryPiData[5]
#                 data = {"device1":d1, "device2":d2, "device3":d3, "device4":d4, "device5":d5}
            data = json.dumps(data)
            return data
        elif(fileName == "init"):
            pass
        else:                                           
            return doSendRegularFiles(fileName)

    @cherrypy.expose
    def default(self, *args, **kwargs):
        try:
            method = cherrypy.request.method
            if method == "GET": 
                z = self.do_GET(args, kwargs)
                return z.encode()
            if method == "POST": 
                self.do_POST(args, kwargs)
        except Exception as e:
            print("*** Error:", e)
            
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

