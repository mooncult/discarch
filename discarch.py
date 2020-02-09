from flask import Flask
from flask import request
import os
import json
import requests
import pdb

app = Flask(__name__)

@app.route('/')
def index():
    return "success! the server is up."


@app.before_request
def log_request_info():
    app.logger.info('Headers: %s', request.headers)
    app.logger.info('Body: %s', request.form.to_dict())


@app.route('/discarch/mention', methods=['post'])
def notify_slack_route():
    response = request.form['challenge']
    return(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
