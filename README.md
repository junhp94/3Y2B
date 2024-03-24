# Speaker Recognition Proof of Concept

This repo tries to implement speaker recognition using the model provided [here](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb). The front end captures the user's voice and sends the audio to the backend, which runs the inference based on the pretrained model. The accuracy is pretty good but it may not be production level.

It is based on [SpeechBrain](https://github.com/speechbrain/speechbrain) which is capable of other tasks such as speech recognition and live transcription.

# Building and Running

Run `pip install -r /path/to/requirements.txt` to install prerequisites and `python app.py` to run the app.
The WS server will be exposed at `localhost:5678/` which you can edit accordingly.

Note: the pretrained model is located under `pretrained_models/` and is ~80MB large. The config file has been modified so that local model will be used instead of downloading from online source, but the `speechbrain` library will still copy and create caches locally at runtime for the first run (not subsequent runs), hence double the space taken.

# Caveats

I noticed the following during development:

- Flask's integration with `WebSocket` was kind of iffy. Two variants of such integration for Flask exist, namely [flask_sockets](https://github.com/heroku-python/flask-sockets) (what I first used; no longer actively developed) and [flask_socketio](https://github.com/miguelgrinberg/Flask-SocketIO). On my front end I based my solution on [JS WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) but obviously there is the other JS client library implementation [Socket.IO](https://socket.io/). `flask_socketio` ended up only working with the latter, but `flask_sockets` seemingly only worked with the former, *and* I ran into the issue where `WebSocket` connection was established and then quickly closed. Debugging led to nowhere. There is also a way of handling WS requests using [gevent.pywsgi](https://snyk.io/advisor/python/gevent/functions/gevent.pywsgi.WSGIServer) which I had no success either. Since `django` has native `websockets` support maybe it is the way to go?

- [Socket.IO](https://socket.io/) *might* not be able to function independently i.e. specify WS address. I kept getting CORS errors from an invalid URL (`localhost/socketIO/randomGibberish`) which wasn't supposed to be there. I assume the webpage isn't meant to be served statically.

- The `SpeechBrain` implementation takes in 2 normalized audio clips (seems to be single channel PCM @ 16Khz) & makes the inference on the fly, so the recorded user's voice has to be stored somewhere and later retrieved for the task. It cannot say assign a "voice fingerprint" in other form, doesn't have production-grade accuracy, and has security / privacy concerns. (If you decrypt / encrypt audio it adds additional time and the audio would have to be saved in memory at some point)

- I based my solution on [this](https://medium.com/@david.richards.tech/how-to-build-a-streaming-whisper-websocket-service-1528b96b1235) which seems a more promising application.
