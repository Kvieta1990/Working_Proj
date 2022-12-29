from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

client = WebClient(token="xoxb-27997197269-4589997032001-J8TqVj7wGnvRDpG7DgMiq6eb")
client.chat_postMessage(channel="memorize", text="Hello world!")
