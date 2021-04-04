import flask
import json

from zomstream import Zomstream

api_version = "0.1"
api = flask.Blueprint('api', __name__)
zomstream = Zomstream()

def construct_response(r):
    # Expecting a JSON-seriazable object as an argument
    # Returning a JSON string with the API response

    # Add Version String
    r.append({"version":api_version})
    return flask.jsonify(r) 

@api.route("/api/stream/", methods = ['GET'])
@api.route("/api/streams/", methods = ['GET'])
def api_list_streams():
    return construct_response(zomstream.getStreams())

@api.route("/api/stream/<app_name>/<stream_name>/", methods = ['GET'])
def api_stream(app_name, stream_name):
    # Filter for streams with 'name' == stream_name
    stream = list(filter(lambda stream: stream['name'] == stream_name, zomstream.getStreams()))
    return construct_response(stream)

