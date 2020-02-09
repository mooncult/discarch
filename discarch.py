#!/usr/bin/env python3
"""This is a app
"""

import argparse
import os
import json
import logging
import pdb
import sys

import requests
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
        convoreps = app.discarch_config['client'].conversations_replies(
            token=app.discarch_config['token'],
            channel=request.json['event']['channel'],
            ts=request.json['event']['thread_ts'])
        inspect(convoreps)
        logging.debug(prettyjson(convoreps))

    msg = "Unhandled condition at path {}. Request data json: {}".format(
        request.path, prettyjson(request.json))
    logging.debug(msg)
    return msg


def main(*args, **kwargs):
    """Main program entrypoint
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", "-t", default=os.environ.get('SLACK_BOT_TOKEN'))
    parser.add_argument("--bindhost", "-b", default="0.0.0.0")
    parser.add_argument("--port", "-p", default="8080")
    parser.add_argument("--debug", "-d", action="store_true")
    parsed = parser.parse_args()
    if not parsed.token:
        raise Exception("You're going to need a token bruh")
    client = slack.WebClient(parsed.token)
    app.discarch_config = {
        'token': parsed.token,
        'client': client,
    }
    app.run(host=parsed.bindhost, port=parsed.port, debug=parsed.debug)


if __name__ == '__main__':
    sys.exit(main(*sys.argv))
