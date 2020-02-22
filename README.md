# The Discussion Archiver

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

## TODO

* [ ] Move `DATABASE` to args format
	* don't require an env
* [ ] Inside `notify_slack_route():` take list of messages from slack api and actually write to db
