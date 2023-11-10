import os
from fastapi import FastAPI
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# uvicorn (in Dockerfile) needs something to run
# we can't pass it the Bolt app
app = FastAPI() 

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN']

# Initializes app with the bot token and socket mode handler
bolt_app = App(token=SLACK_BOT_TOKEN)

@bolt_app.event("message")
def say_hello(message, say):
    text = message['text']
    say(f"Getting the answer for you! {text}")

# Start the Slack bolt app to interact via websockets
SocketModeHandler(bolt_app, SLACK_APP_TOKEN).start()