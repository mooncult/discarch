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


logger = logging.getLogger(__name__)
app = Flask(__name__)


class SlackMessage():
    def __init__(self, json_string):
        self.team = json_string['team']
        self.user_id = json_string['user']
        self.parent_user = json_string['parent_user_id']
        self.thread_ts = json_string['thread_ts']
        self.ts = json_string['ts']
        


def prettyjson(obj):
    return json.dumps(obj, indent=2, sort_keys=True)


def inspect(title, something):
    logger.debug("<{}> Type: {}".format(title, type(something)))
    logger.debug("<{}> Dir: {}".format(title, dir(something)))
    logger.debug("<{}> Value: {}".format(title, something))


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
    logger.debug("JSON object at request.json: {}".format(prettyjson(request.json)))
    if 'challenge' in request.json:
        return request.json['challenge']
    elif 'event' in request.json and request.json['event']['type'] == 'app_mention':
        logger.debug("I think this is the event you get when you get app mentioned")
        logger.debug(request.json['event']['text'])
        if 'thread_ts' not in request.json['event']:
            msg = "Got my @ss @'d outside of a thread, no one cares lol"
            logger.info(msg)
            return msg
        logger.debug("Trynna unroll thread with thread_ts: {}".format(
            request.json['event']['thread_ts']))
        convoreps = app.discarch_config['client'].conversations_replies(
            token=app.discarch_config['token'],
            channel=request.json['event']['channel'],
            ts=request.json['event']['thread_ts'])
        inspect("convoreps", convoreps)
        inspect("convoreps.data", convoreps.data)
        logger.debug(prettyjson(convoreps.data))
        return "OK"

    msg = "Unhandled condition at path {}. Request data json: {}".format(
        request.path, prettyjson(request.json))
    logger.debug(msg)
    return msg


def main(*args, **kwargs):
    """Main program entrypoint
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", "-t", default=os.environ.get('SLACK_BOT_TOKEN'))
    parser.add_argument("--bindhost", "-b", default="0.0.0.0")
    parser.add_argument("--port", "-p", default="8080")
    parser.add_argument("--debug", "-d", action="store_true")
    parser.add_argument("--logfile", "-l")
    parsed = parser.parse_args()
    loglevel = logging.INFO
    if parsed.debug:
        loglevel = logging.DEBUG
    logger.setLevel(loglevel)
    if parsed.logfile:
        fh = logging.FileHandler(parsed.logfile)
        fh.setLevel(loglevel)
        logger.addHandler(fh)
    logger.debug("Configured logging, nice")
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
