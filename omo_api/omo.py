""" Basic operations using Slack_sdk """

import os
from slack_sdk import WebClient 
from slack_sdk.errors import SlackApiError 

""" We need to pass the 'Bot User OAuth Token' """
#slack_token = os.environ.get('SLACK_BOT_TOKEN')
slack_token = 'xoxb-2491940513286-6128114798339-UCcWeY6ZZQ5WWUPmbuqympYM'

# Creating an instance of the Webclient class
client = WebClient(token=slack_token)

try:
	# Posting a message in #random channel
	response = client.chat_postMessage(
    				channel="general",
    				text="Bot's first message")
	
	# Get a list of conversations
	response = client.conversations_list()
	print(response["channels"])
	
except SlackApiError as e:
	assert e.response["error"]