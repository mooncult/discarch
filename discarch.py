#!/usr/bin/env python3

import argparse
import logging
import sys

import slack


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def idb_excepthook(type, value, tb):
    """Call an interactive debugger in post-mortem mode

    If you do "sys.excepthook = idb_excepthook", then an interactive debugger
    will be spawned at an unhandled exception
    """
    if hasattr(sys, 'ps1') or not sys.stderr.isatty():
        sys.__excepthook__(type, value, tb)
    else:
        import pdb, traceback
        traceback.print_exception(type, value, tb)
        print
        pdb.pm()


@slack.RTMClient.run_on(event='message')
def handle_messages(**payload):
    """
    Does a lot. Fucking decorators.
    1. if the message has react-able strings, react to the message appropriately
    2. if the message starts with @botname and has a command i've planned for, do thing.
    """
    data = payload['data']
    channel_id = data['channel']
    thread_ts = data['ts']

    if not data['text'].startswith("MOONRITUAL"):
        return
    response = "🧞‍♀️"

    webclient = payload['web_client']
    webclient.chat_postMessage(
        channel=channel_id,
        text=response,
        timestamp=thread_ts
    )


def main(*args, **kwargs):
    parser = argparse.ArgumentParser(
        description="The Dicussion Archiver")
    parser.add_argument(
        "--debug", "-d", action='store_true',
        help="Include debugging output")
    parser.add_argument(
        "--api-token", "-t", required=True, help="Slack API token")
    parsed = parser.parse_args()
    if parsed.debug:
        sys.excepthook = idb_excepthook
        LOGGER.setLevel(logging.DEBUG)

    rtm_client = slack.RTMClient(token=parsed.api_token)
    rtm_client.start()


if __name__ == '__main__':
    sys.exit(main(*sys.argv))
