from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

client = WebClient(token="xoxb-27997197269-4579628452532-KfsiDmfcu70kAv9HU12zo2jb")
client.chat_postMessage(channel="words", text="Hello world!")
