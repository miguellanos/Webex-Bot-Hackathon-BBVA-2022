from webexteamsbot import TeamsBot
from webexteamsbot.models import Response
from dotenv import load_dotenv
from loguru import logger
import requests
import os
import json
import re

load_dotenv()
WEBHOOKURL = os.getenv("TEAMS_BOT_URL")
logger.debug(WEBHOOKURL)
BOTEMAIL = os.getenv("TEAMS_BOT_EMAIL")
TEAMSTOKEN = os.getenv("WEBEX_TEAMS_ACCESS_TOKEN")
TETOKEN = os.getenv("TETOKEN")
bot_app_name = os.getenv("TEAMS_BOT_APP_NAME")
message = ""
base_url = "https://api.thousandeyes.com/v6/"
# Create a Bot Object
bot = TeamsBot(
    bot_app_name,
    teams_bot_token=TEAMSTOKEN,
    teams_bot_url=WEBHOOKURL,
    teams_bot_email=BOTEMAIL,
    debug=True,
    webhook_resource_event=[
        {"resource": "messages", "event": "created"},
    ],
)

headers = {
        "Authorization": "Bearer "+ TETOKEN,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }


# A simple command that returns a basic string that will be sent as a reply
def list_agents(incoming_msg):
    message="Here is your list of agents:<br /><br />"
    res = requests.get(url=base_url+"endpoint-agents", headers=headers)
    data = json.loads(res.text)
    for agent in data['endpointAgents']:
        message = message+(f"Agent Name: {agent['agentName']} - Type: {agent['agentType']}<br />")
    return message

def list_tests(incoming_msg):
    message="Here is your list of tests:<br /><br />"
    res = requests.get(url=base_url+"tests", headers=headers)
    data = json.loads(res.text)
    for test in data['test']:
        message = message+(f"Test ID: {test['testId']} - Type: {test['type']} - Test Name: {test['testName']}<br />")
    return message

def test_details(incoming_msg):
    message = incoming_msg.text
    test_id = str(re.sub('[^0-9]','', message))
    res = requests.get(url=base_url+"tests/"+test_id, headers=headers)
    data = json.loads(res.text)
    for test in data['test']:
        message = f"""Test ID: {test['testId']}
                    Type: {test['type']}
                    Test Name: {test['testName']}
                    URL: {test['url']}
                    Protocol: {test['protocol']}
                    Interval: {test['interval']}
                    Path Traces: {test['numPathTraces']}"""
    return message

# Add new commands to the box.
bot.add_command("/listagents", "This will list endpoint agents", list_agents)
bot.add_command("/listtests", "This will list tests", list_tests)
bot.add_command("/testdetails", "This will provde more information about a test with the given Test ID (e.g. /testdetails 12345)", test_details)

bot.remove_command("/echo")


if __name__ == "__main__":
    # Run Bot
    bot.run(host="0.0.0.0", port=8181)