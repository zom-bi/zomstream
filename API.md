# ZomStream API
Zomstream provides a RESTful API that can be used to query for streams.
As of API version 0.2, there are two API endpoints:
## List of active streams
You can query for a list of active streams, by sending a GET request to
`localhost:8080/api/streams/`
Here's an example query and the expected result:

`$ curl http://localhost:8080/api/v0.2/streams/`
Response example:
```json
{
"streams":
        [
                {"app":"live","name":"foo"},
                {"app":"live","name":"bar"}
        ]
}

```
i.e. There are two active streams in the `live` app, namely foo and bar. More information about the streams can be queried as follows.

## Query Stream information
If you know the app and name of the stream you want to query, you can request more information,with a query like this:
`$ curl http://localhost:8080/api/v0.2/streams/foo/`
Response example:
```json
{
"streams":{
                "app":"live",
                "name":"foo",
                "urls":
                        [
                                {"type":"http_flv","url":"https://localhost:8080/flv?app=live&stream=foo"},
                                {"type":"rtmp","url":"rtmp://localhost/live/foo"}
                        ]
        }
}

```
