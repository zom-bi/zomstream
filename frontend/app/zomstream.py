import pathlib
import xml.etree.ElementTree as etree
import sys
import yaml
import urllib


class Stream:
    def __init__(self, app, name, urls):
        self.name = name  # String
        self.app = app    # String
        self.urls = urls  # List of Dictionaries with the keys url and type


class Zomstream:
    def __init__(self):
        # load configuration from config.yml file
        if pathlib.Path("config.yml").is_file():
            stream = open('config.yml', 'r')
            self.configuration = yaml.load(stream)
            stream.close()
        else:
            print('missing configuration.')
            sys.exit(1)
        self.streamnames = []

    def getStreamNames(self):
        self.streamnames = []
        # get data from the streaming server
        response = urllib.request.urlopen(self.configuration['stat_url'])
        content = response.read().decode('utf-8')
        # parse the xml / walk the tree
        tree = etree.fromstring(content)
        server = tree.find('server')
        applications = server.findall('application')
        for application in applications:
            appname = application.find('name')
            if appname.text == "live" or appname.text == "rec":
                streams = application.find('live').findall('stream')
                for stream in streams:
                    name = stream.find('name')
                    rate = stream.find('bw_video')
                    if rate.text != "0":
                        self.streamnames.append( [appname.text, name.text] )
    
        return self.streamnames
        
        
    def getStreams(self):
        streams = []
        for streamName in self.getStreamNames():
            urls = []
            app  = streamName[0]
            name = streamName[1]

            flv_url  = self.getFlvUrl (app,name)
            rtmp_url = self.getRtmpUrl(app,name)

            urls.append({'url': flv_url, 'type':'http_flv'})
            urls.append({'url': rtmp_url,'type':'rtmp'})

            stream = Stream(app=app, name=name, urls=urls)
            streams.append(stream.__dict__)
        return streams

    def getFlvUrl(self,app_name,stream_name):
        return '%s://%s/flv?app=%s&stream=%s' % (
            self.configuration['web_proto'],
            self.configuration['base_url'],
            app_name,
            stream_name)
    def getRtmpUrl(self,app_name,stream_name):
        return "rtmp://%s/%s/%s" % (
            self.configuration['rtmp_base'],
            app_name,
            stream_name)
