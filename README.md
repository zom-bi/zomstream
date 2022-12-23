# ZomStream
Zomstream is a web frontend for streaming video. We wrote it as we needed a overview of the running streams on our nginx-rtmp Server.

It is written in python3 and based on the flask microframework and does not need any databases or other external Services. It does not store any persistent data and its only configuration are some parameters in the docker compose file and a simple configuration file for the webfrontend.

It currently uses RTMP and http-flv for Stream Delivery. The latter can be played on the Webpage using a flv.js based player utilizing the Media Source Extensions API.

This repository does contain all needed components for a "streaming server in a box" Setup.

## Credits
 * We are using the flv.js library (https://github.com/bilibili/flv.js) for our webplayer
 * The included Streaming Server is based on nginx (https://nginx.org) with the nginx-http-flv-module (https://github.com/winshining/nginx-http-flv-module)

## Components
Zomstream is a multiple container setup which should be setup using docker-compose. It consists of the following components.

### nginx-rtmp
nginx webserver with rtmp/flv patches.

this does run the actual streaming, receives rtmp streams from OBS / ffmpeg etc. and provides the streams in rtmp or http-flv format for web based players.

### auth
this is a simple PSK based authentication module to provide authentication for source connections.

### frontend
this components provides the visible website containing an overview of the running streams, a REST API,  rtmp links for external players and a web based video player to watch the livestreams.
There is more information about the API in [API.md](API.md) 

## How to use this
We tested this with OBS and ffmpeg but any streaming source supporting rtmp should work just fine.

### Setup instructions
* clone the repository
* copy the file `frontend/config.example.yml` to `frontend/config.yml`
* modify this configuration file (especially the parameters `rtmp_base`, `base_url` and `web_proto`)
* copy the `docker-compose.default.yml` to `docker-compose.yml`
  * uncomment the traefik parameters or the port forward of port 8080 of the webserver depending on your setup
  * set the PSK stream password in the `password` environment variable of the `auth` container.
* run `docker-compose up -d` to build and start the containers


### Example Setup using OBS:
* Go to "Settings" -> "Stream"
* Set the "Stream Type" to "Custom Streaming Server"
* enter your Hostname or IP and the Service "live" in the URL Field if you want to have the Stream listed on the Webpage
  * example: `rtmp://127.0.0.1/live`
* you can also use the Service "unlisted" to hide your stream in the stream list
  * example: `rtmp://127.0.0.1/unlisted`
* Enter your desired Streamname and the Authentication Information for the auth container in the "Stream Key" field
  * example: `stream?pass=password1234`
* your stream should be accessible on `http://127.0.0.1:8080/player/live/stream` or `http://127.0.0.1/player/unlisted/stream` depending on the application. If you used the `live` application the stream should also be listed on the index page.
