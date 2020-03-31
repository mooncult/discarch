#!/usr/bin/env python3

import unittest
import json

import discarch


class MockRequest:

    def __init__(self, js):
        self.json = js


class ChallengeTestCase(unittest.TestCase):

    def test_process_challenge(self):
        challenge_dict = {
            "challenge": "bh8f02by4W5q5HUedMU5Ugq94j1kiv3RJgNeCHacx5TVQxJUsFQB",
            "token": "3z3jGGlzw9RAxNSZiUuQcfqr",
            "type": "url_verification"
        }

        req = MockRequest(challenge_dict)

        self.assertEqual(discarch.process_challenge(req), challenge_dict['challenge'])


class SlackMessageTestCase(unittest.TestCase):


    def test_event_subscription_dispatcher_challenge(self):
        # mock a slack challenge.
        slack_challenge = {
            "token": "Jhj5dZrVaK7ZwHHjRyZWjbDl",
            "challenge": "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P",
            "type": "url_verification"
        }

        challenge_req = MockRequest(slack_challenge)
        self.assertEqual(discarch.event_subscription_dispatcher(challenge_req), discarch.process_challenge)

    def test_event_subscription_dispatcher_mention(self):
        # mock a slack message containing a mention.
        slack_mention = {
            "token": "ZZZZZZWSxiZZZ2yIvs3peJ",
            "team_id": "T061EG9R6",
            "api_app_id": "A0MDYCDME",
            "event": {
                "type": "app_mention",
                "user": "U061F7AUR",
                "text": "What ever happened to <@U0LAN0Z89>?",
                "ts": "1515449438.000011",
                "channel": "C0LAN2Q65",
                "event_ts": "1515449438000011"
            },
            "type": "event_callback",
            "event_id": "Ev0MDYGDKJ",
            "event_time": 1515449438000011,
            "authed_users": [
                "U0LAN0Z89"
            ]
        }
        mention_req = MockRequest(slack_mention)
        self.assertEqual(discarch.event_subscription_dispatcher(mention_req), discarch.process_app_mention_event)
