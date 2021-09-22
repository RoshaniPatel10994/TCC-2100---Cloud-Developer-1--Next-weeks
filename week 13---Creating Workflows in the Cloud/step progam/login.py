from datetime import datetime
import logging
import boto3
from datetime import datetime

logger = logging.getlogger()
logger.setLevel(logging.INFO)

ENDPOINT = arn:aws:dynamodb:us-east-2:748939641058:table/DogTreats
TABLE_NAME = "DogTreats"

class LoginException(Exception):
    pass

def log_in_out(username,action):

    time_stamp = datetime.now().strftime("%m/%d/%y, %h/%m/%s")

    try:
        db_client = boto3.client("dynamodb")
        db_client.update_item(
            TableName=Table_Name,
            Key={
                "pk": {"S": username},
                "sk": {"S": action},
            },
            UpdateExpression="Add time_stamp :ts",
            ExpressionAttributeValues={"ts": {"SS": [time_stamp]}}
        )

    except Exception as e:
        logging.error(e)

def lambda_handler(event, _):

    logger.info(event["Input"])
    logger.info(event["Input"]["username"])
    logger.info(event["Input"]["action"])

    username = event['Input']["username"]
    action = event["Input"]["action"]

    try:
        log_in_out(username, action)
        return {"status": "success", "action": action}
    except Exception:
        raise LoginException("Login/out action failed!")

if _name_ == "_main_":

    mock_event = {"input": {"username": "roshani", "action": "logout"}}

    print(lambda_handler(mock_event, None))

    


