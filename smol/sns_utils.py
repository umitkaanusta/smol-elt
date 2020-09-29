import boto3
import json
from datetime import datetime

with open("../credentials/aws_credentials.json") as credfile:
    cred = json.load(credfile)
    access_key = cred["access_key"]
    secret_key = cred["secret_key"]

sns = boto3.client(
    "sns",
    region_name="us-east-1",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)

reload_success = sns.create_topic(Name="reload-success")  # Change the topic name if you want

# You can subscribe your email address thru AWS Console too
# sub = sns.subscribe(
#    TopicArn=reload_success["TopicArn"],
#    Protocol="email",
#    Endpoint="user@email.com"
# )


def send_success_message():
    sns.publish(
        TopicArn=reload_success["TopicArn"],
        Message=f"""The spreadsheet Python.org Jobs has been successfully reloaded.
        Update time: {datetime.now()}""",
        Subject="Reload successful - Python.org Jobs"
    )


def send_failure_message(old_state, new_state):
    sns.publish(
        TopicArn=reload_success["TopicArn"],
        Message=f"""There is a problem on the pipeline for the Python.org Jobs spreadsheet.
            Update time: {datetime.now()}
            Task: {old_state}
            Error: {new_state}""",
        Subject="Reload FAILED - Python.org Jobs"
    )
    quit(1)
