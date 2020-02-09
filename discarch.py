#!/usr/bin/env python3
"""This is a app
"""

import os
import json
import logging
import requests
import pdb

from flask import Flask
from flask import request


logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)


def inspect(something):
    logging.debug("Type: {}".format(type(something)))
    logging.debug("Dir: {}".format(dir(something)))
    logging.debug("Value: {}".format(something))


@app.route('/')
def index():
    return "success! the server is up."


@app.before_request
def log_request_info():
    app.logger.info('Headers: %s', request.headers)
    app.logger.info('Body: %s', request.form.to_dict())


@app.route('/discarch/mention', methods=['POST'])
def notify_slack_route():
    inspect(request)
    data = request.json
    response = data['challenge']
    return(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
