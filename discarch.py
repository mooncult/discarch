from flask import Flask
from flask import request
import os
import json
import requests
import pdb

app = Flask(__name__)


@app.route('/awspath')
def lb_check():
    return 'this is the index route'


@app.route('/')
def index():
    return 'this is garbage. you probably meant to hit a different url.'


@app.before_request
def log_request_info():
    app.logger.info('Headers: %s', request.headers)
    app.logger.info('Body: %s', request.form.to_dict())


@app.route('/discarch/mention', methods=['post'])
def notify_slack_route():
    post_json = request.form.to_dict(flat=False)
    # this houses the json dict
    convert_to_json = json.loads(post_json['payload'][0])
    # this is the callback_id needed for later API calls
    callback_id = convert_to_json.get('callback_id')
    # this is the original message which can be modified for replacement
    original_message = convert_to_json.get('original_message')
    slack_attachments = [
    {
        "fallback": "buttons didn't work.",
        "text": "BUTTONS.",
        "attachment_type": "default",
        "callback_id": 'non-unique',
        "actions": [
            {
            "type": "button",
            "text": "View investigation",
            "url": 'https://me.jowj.net',
            "style": "primary"
            },
            {
            "type": "section",
            "text": "BUTTONS."
            }
        ]
        }
    ]
    # actually close the specified investigation.
    original_message['attachments'] = slack_attachments
    response = convert_to_json.get('original_message')
    return(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
