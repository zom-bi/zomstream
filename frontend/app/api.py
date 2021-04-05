import flask
import json

from zomstream import Zomstream

api_version = "0.2"
api_base = "/api/v" + api_version

api = flask.Blueprint('api', __name__)
zomstream = Zomstream()

def construct_response(streams):
    # Expecting a JSON-serializable list as an argument
    # Returning a JSON string with the API response

    r = {"streams":streams}
    return flask.jsonify(r)

@api.route(api_base + "/streams/", methods = ['GET'])
def api_list_streams():
    streams = []
    for stream in zomstream.getStreamNames():
        streams.append({'app':stream[0],'name':stream[1]})
    return construct_response(streams)


@api.route(api_base + "/streams/<stream_name>/", methods = ['GET'])
def api_stream( stream_name):
    # Filter for streams with 'name' == stream_name
    stream = list(filter(lambda stream: stream['name'] == stream_name, zomstream.getStreams()))
    return construct_response(stream)
