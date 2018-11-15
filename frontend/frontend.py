#!/usr/bin/env python

# imports
import flask
import pathlib
import yaml
import sys
import xml.etree.ElementTree as etree
import urllib
import logging

logging.basicConfig(level=logging.DEBUG)

# for populating stream list in background
import threading
import time

# load configuration from config.yml file
if pathlib.Path("config.yml").is_file():
    stream = open('config.yml', 'r')
    configuration = yaml.load(stream)
    stream.close()
else:
    print('missing configuration.')
    sys.exit(1)

def getStreamNames(url):
    streamnames = []
    # get data from the streaming server
    response = urllib.request.urlopen(url)
    content = response.read().decode('utf-8')
    # parse the xml / walk the tree
    tree = etree.fromstring(content)
    server = tree.find('server')
    application = server.find('application')
    appname = application.find('name')
    if appname.text == "live":
        live = application.find('live')
        streams = live.findall('stream')
        for stream in streams:
            name = stream.find('name')
            rate = stream.find('bw_video')
            if rate.text != "0":
                streamnames.append(name.text)
    return streamnames

streamList = []
frontend = flask.Flask(__name__)

@frontend.before_first_request
def populate_streamlist():
    def streamlist_loop():
        global streamList
        while True:
            streamList = getStreamNames(configuration['stat_url'])
            frontend.logger.info('updated streamlist: ' + str(streamList))
            time.sleep(10)
    thread = threading.Thread(target=streamlist_loop)
    thread.start()

@frontend.route("/")
def start():
    mainTemplate = '%s/main.html.j2' % configuration['template_folder']
    page = flask.render_template(
        mainTemplate,
        items=streamList,
        configuration=configuration
    )
    return page

@frontend.route("/player/<streamname>")
def show_player(streamname):
    playerTemplate = '%s/player.html.j2' % configuration['template_folder']
    page = flask.render_template(
        playerTemplate, 
        name=streamname,
        hls_url='%s://%s/video/hls/%s.m3u8' % (
            configuration['web_proto'], 
            configuration['base_url'], 
            streamname),
        configuration=configuration
        )
    return page
