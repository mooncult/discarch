#!/usr/bin/env python3
"""This is a app
"""

import os
import json
import logging
import requests
import pdb

import slack
from flask import Flask
from flask import request


logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)


def prettyjson(obj):
    return json.dumps(obj, indent=2, sort_keys=True)


def inspect(title, something):
    logging.debug("<{}> Type: {}".format(title, type(something)))
    logging.debug("<{}> Dir: {}".format(title, dir(something)))
    logging.debug("<{}> Value: {}".format(title, something))


@app.route('/')
def index():
    return "success! the server is up."


@app.before_request
def log_request_info():
    app.logger.info('Headers: %s', request.headers)
    app.logger.info('Body: %s', request.form.to_dict())


@app.route('/discarch/mention', methods=['POST'])
def notify_slack_route():
    inspect("req", request)
    inspect("path", request.path)
    logging.debug("JSON object at request.json: {}".format(prettyjson(request.json)))
    if 'challenge' in request.json:
        return request.json['challenge']
    elif 'event' in request.json and request.json['event']['type'] == 'app_mention':
        logging.debug("I think this is the event you get when you get app mentioned")
        logging.debug(request.json['event']['text'])
        if 'thread_ts' not in request.json['event']:
            msg = "Got my @ss @'d outside of a thread, no one cares lol"
            logging.info(msg)
            return msg
        logging.debug("Trynna unroll thread with thread_ts: {}".format(
            request.json['event']['thread_ts']))
        logging.debug(CLIENT.conversations_replies(
            token=TOKEN,
            channel=request.json['event']['channel'],
            ts=request.json['event']['thread_ts'])
        )

    msg = "Unhandled condition at path {}. Request data json: {}".format(
        request.path, prettyjson(request.json))
    logging.debug(msg)
    return msg


if __name__ == '__main__':
    TOKEN = os.environ['SLACK_BOT_TOKEN']
    CLIENT = slack.WebClient(TOKEN)    
    app.run(host='0.0.0.0', port='8080', debug=True)
