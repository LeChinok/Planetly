from flask import Flask, jsonify, request, render_template, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
from time import time, sleep
from models import Home

app = Flask(__name__)

limiter = Limiter(app, key_func=get_remote_address)

# default request limit, 2 request/second
rate = "2/second"

@app.route("/")
# index endpoint
def index():
  model = Home()
  return render_template('index.html',model=model)

# function to change the request limit
def rate_limit():
  return app.config.get("CUSTOM_LIMIT", rate)

# /ping endpoint
@app.route("/ping")
# request limit, take from rate_limit function
@limiter.limit(rate_limit)
def ping():
  get_time_req = request.headers.get('time_req')
  time_req = int(get_time_req)
  # will run a request every 1 second
  time_def = sleep(time_req)
  # retrieve secret key from headers
  data = request.headers.get('x_secret_key')
  # valid secret key, key-123
  key = 'key-123'

  # if the secret key taken from the headers is the same as the valid secret key
  if data == key:
    # create global variable
    global rate
    # change the request limit to 10 requests/minute
    rate = "9/minute"
    return jsonify(message='pong')
  # if the secret key retrieved from the header is not the same as the valid secret key 
  # then the request limit will still be 2 requests/second
  else:
    return jsonify(message='pong')

# if the limit request has been reached
# call error handler
@app.errorhandler(429)
def ratelimit_handler(e):
  # displays the time limit request has been reached
  date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
  return jsonify(throttle_age=date, message="request limit")

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000)
