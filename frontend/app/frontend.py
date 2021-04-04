#!/usr/bin/env python3

# imports
import flask
import urllib
from zomstream import Zomstream

streamList = []
zomstream = Zomstream()

frontend = flask.Blueprint('frontend', __name__)

@frontend.route("/")
def start():
    mainTemplate = '%s/main.html.j2' % zomstream.configuration['template_folder']
    streamList = zomstream.getStreamNames()
    page = flask.render_template(
        mainTemplate,
        items=streamList,
        configuration=zomstream.configuration
    )
    return page

@frontend.route("/player/<appname>/<streamname>")
def show_player(appname, streamname):
    playerTemplate = '%s/player.html.j2' % zomstream.configuration['template_folder']
    page = flask.render_template(
        playerTemplate, 
        streamname=streamname,
        appname=appname,
        configuration=zomstream.configuration
        )
    return page
