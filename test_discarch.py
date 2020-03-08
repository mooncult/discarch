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


