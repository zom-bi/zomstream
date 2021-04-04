import flask
import urllib
import frontend
import api

import logging
logging.basicConfig(level=logging.DEBUG)

web = flask.Flask(__name__)
web.register_blueprint(api.api)
web.register_blueprint(frontend.frontend)
