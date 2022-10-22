from webexteamsbot import TeamsBot
from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()
WEBHOOKURL = os.getenv("TEAMS_BOT_URL")
BOTEMAIL = os.getenv("TEAMS_BOT_EMAIL")
TEAMSTOKEN = os.getenv("WEBEX_TEAMS_ACCESS_TOKEN")
TETOKEN = os.getenv("TETOKEN")
BOTAPPNAME = os.getenv("TEAMS_BOT_APP_NAME")

base_url = "https://api.thousandeyes.com/v6/"

# Create a Bot Object
bot = TeamsBot(
    BOTAPPNAME,
    teams_bot_token=TEAMSTOKEN,
    teams_bot_url=WEBHOOKURL,
    teams_bot_email=BOTEMAIL,
    debug=True,
    webhook_resource_event=[
        {"resource": "messages", "event": "created"},
    ],
)

TE_headers = {
        "Authorization": "Bearer "+ TETOKEN,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

# A simple command that returns a basic string that will be sent as a reply
def list_agents(incoming_msg):
    res = requests.get(url=base_url+"endpoint-agents", headers=TE_headers)
    data = json.loads(res.text)
    message="Here is your list of agents:<br /><br />"
    for agent in data['endpointAgents']:
        message = message+(f"Agent Name: {agent['agentName']} - Type: {agent['agentType']}<br />")
    return message

# Add new commands to the box.
bot.add_command("/listagents", "List endpoint agents", list_agents)

if __name__ == "__main__":
    # Run Bot
    bot.run(host="0.0.0.0", port=8181)
