# ZomStream
Zomstream is a web frontend for streaming video. We wrote it as we needed a overview of the running streams on our nginx-rtmp Server.

It is written in python and based on the flask microframework and does not need any databases or other external Services. It does not store any persistent data and its only configuration are some parameters in the docker compose file and a simple configuration file for the webfrontend.

This repository does contain all needed components for a "streaming server in a box" Setup.

## Credits
 * We are using the hls.js library (https://github.com/video-dev/hls.js/) for our webplayer
 * The Included Streaming Server is based on nginx (https://nginx.org) with the nginx rtmp patches (https://github.com/arut/nginx-rtmp-module)


## Components
Zomstream is a multiple container setup which should be setup using docker-compose. It consists of the following components.

### nginx-rtmp
nginx webserver with rtmp patches.

this does run the actual streaming, receives rtmp streams from OBS / ffmpeg etc. and provides the streams in hls or dash format for web based players.

### auth
this is a simple PSK based authentication module to provide authentication for source connections.

### frontend
this components provides the visible website containing a overview of the running streams, rtmp links for external players and a web based video player to watch the livestreams.

## How to use this
We tested this with OBS and ffmpeg but any steaming source supporting rtmp should work just fine.

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
* enter your Hostname or IP and the Service "live" in the URL Field
  * example: `rtmp://127.0.0.1/live`
* Enter your desired Streamname and the Authentication Information for the auth container in the "Stream Key" field
  * example: `stream?pass=password1234`

