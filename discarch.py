#!/usr/bin/env python3
"""This is a app
"""

import argparse
import os
import json
import logging
import sys
import sqlite3

import requests
import slack
from flask import Flask
from flask import request

logger = logging.getLogger(__name__)
app = Flask(__name__)


def get_db():
    db = getattr(app, '_database', None)
    if db is None:
        db = app._discarch_database = sqlite3.connect(app._discarch_dbpath)
    return db


def init_db():
    cur = get_db().cursor()
    cur.execute('''CREATE TABLE messages
    (thread_ts, message_ts, user, team, message_text)''')


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(app, '_database', None)
    if db is not None:
        db.close()


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


def process_challenge(request):
    """process a challenge from slack event subscription
    expects a request object from flask
    """
    return request.json['challenge']


def process_app_mention_event(request):
    """process an app mention event from slack event sub
    expects a request object from flask
    """
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

    logger.debug(prettyjson(convoreps.data))

    cur = get_db().cursor()
    for thing in convoreps:
        """ if a message.ts exists in db do nothing. else, save it
        """
        pass

    return "OK"


@app.route('/discarch', methods=['POST'])
def discarch_main():
    """the main function for the discarch route url
    """
    msg = f"i'm in discarch_main, and here's my shit: {request}"

    try:
        decoded = prettyjson(request.json)
        msg += decoded
    except Exception as e:
        msg += f"we couldn't decode json because: {e}"

    logger.debug(msg)
    processor = event_subscription_dispatcher(request)
    return processor(request)


def event_subscription_dispatcher(request):
    """dispatch events from slack

    given a request that (came from flask) return the appropriate action.
    return something even if the conditions we don't care about aren't met 
    due to flask requirements
    """
    logger.debug("JSON object at request.json: {}".format(prettyjson(request.json)))    
    if 'challenge' in request.json:
        return process_challenge
    elif 'event' in request.json and request.json['event']['type'] == 'app_mention':
        return process_app_mention_event
    else:
        msg = "Unhandled condition at path {}. Request data json: {}".format(
            request.path, prettyjson(request.json))
        logger.debug(msg)
        return msg


def main(*args, **kwargs):
    """Main program entrypoint
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", "-t", default=os.environ.get('SLACK_BOT_TOKEN'))
    parser.add_argument("--database", "-db", default=os.environ.get('SQL_DB_NAME'))
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
    init_db()
    app._discarch_dbpath = parsed.database
    app.run(host=parsed.bindhost, port=parsed.port, debug=parsed.debug)


if __name__ == '__main__':
    sys.exit(main(*sys.argv))
