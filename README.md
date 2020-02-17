n# The Discussion Archiver

This bot will archive threads in Slack.
Sort of like <https://threadreaderapp.com/> on Twitter.

It doesn't work yet.

## Slack configuration

This bot currently uses the RTM API.
This means you canNOT use a new style Slack app -
you must use a "classic" Slack app.

You cannot create a classic Slack app on
<https://api.slack.com/apps?new_classic_app=1>;
you must click the "Create a classic Slack app" button from this page:
<https://api.slack.com/rtm>,
or use this URL:
<https://api.slack.com/apps?new_classic_app=1>

New style Slack apps have only ONE token on their "Install App" page,
with the title "Bot User OAuth Access Token".
Old style Slack apps have TWO tokens on that page,
one with the title "OAuth Access Token"
and the other with the title "Bot User OAuth Access Token".
You need the OAuth token from the old style app.
If you try to use a new style app's oauth token,
you will not be able to `rtm_client.start()`;
you will get an exception with a message like
`The server responded with: {'ok': False, 'error': 'invalid_auth'}`.

## Example slack message
```json
DEBug:root:{
  "has_more": false,
  "messages": [
    {
      "blocks": [
        {
          "block_id": "b89",
          "elements": [
            {
              "elements": [
                {
                  "text": "nice lol",
                  "type": "text"
                }
              ],
              "type": "rich_text_section"
            }
          ],
          "type": "rich_text"
        }
      ],
      "client_msg_id": "f3d5d3ef-37aa-4fb4-a39e-62c4d1cc02b1",
      "latest_reply": "1581903932.064500",
      "replies": [
        {
          "ts": "1581903369.064100",
          "user": "U16H7LW56"
        },
        {
          "ts": "1581903455.064300",
          "user": "U16H7LW56"
        },
        {
          "ts": "1581903932.064500",
          "user": "U16H7LW56"
        }
      ],
      "reply_count": 3,
      "reply_users": [
        "U16H7LW56"
      ],
      "reply_users_count": 1,
      "subscribed": false,
      "team": "T0WCHAYQN",
      "text": "nice lol",
      "thread_ts": "1581386181.063100",
      "ts": "1581386181.063100",
      "type": "message",
      "user": "U16H7LW56"
    },
    {
      "blocks": [
        {
          "block_id": "IyzT",
          "elements": [
            {
              "elements": [
                {
                  "type": "user",
                  "user_id": "UTRGHNCCQ"
                },
                {
                  "text": " its a thread bitch",
                  "type": "text"
                }
              ],
              "type": "rich_text_section"
            }
          ],
          "type": "rich_text"
        }
      ],
      "client_msg_id": "8c636961-fcc9-478b-8555-016ae9212ff1",
      "parent_user_id": "U16H7LW56",
      "team": "T0WCHAYQN",
      "text": "<@UTRGHNCCQ> its a thread bitch",
      "thread_ts": "1581386181.063100",
      "ts": "1581903369.064100",
      "type": "message",
      "user": "U16H7LW56"
    },
    {
      "blocks": [
        {
          "block_id": "yf5",
          "elements": [
            {
              "elements": [
                {
                  "type": "user",
                  "user_id": "UTRGHNCCQ"
                },
                {
                  "text": " thread message 2 fucker",
                  "type": "text"
                }
              ],
              "type": "rich_text_section"
            }
          ],
          "type": "rich_text"
        }
      ],
      "client_msg_id": "f464f929-ce10-4391-901b-bf7fd12277d4",
      "parent_user_id": "U16H7LW56",
      "team": "T0WCHAYQN",
      "text": "<@UTRGHNCCQ> thread message 2 fucker",
      "thread_ts": "1581386181.063100",
      "ts": "1581903455.064300",
      "type": "message",
      "user": "U16H7LW56"
    },
    {
      "blocks": [
        {
          "block_id": "j6M/b",
          "elements": [
            {
              "elements": [
                {
                  "type": "user",
                  "user_id": "UTRGHNCCQ"
                },
                {
                  "text": "  thread message 3 asshole",
                  "type": "text"
                }
              ],
              "type": "rich_text_section"
            }
          ],
          "type": "rich_text"
        }
      ],
      "client_msg_id": "ac879da1-0032-4296-93b3-596fbf09d646",
      "parent_user_id": "U16H7LW56",
      "team": "T0WCHAYQN",
      "text": "<@UTRGHNCCQ>  thread message 3 asshole",
      "thread_ts": "1581386181.063100",
      "ts": "1581903932.064500",
      "type": "message",
      "user": "U16H7LW56"
    }
  ],
  "ok": true
}
```

## TODO

[ ] Move `DATABASE` to args format
	* don't require an env
[ ] Inside `notify_slack_route():` take list of messages from slack api and actually write to db
