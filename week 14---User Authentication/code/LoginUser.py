import boto3
import json
from pprint import pprint
from aws_srp import AWSSRP
from botocore.exceptions import ClientError

USERNAME = input('Enter your username: ')
PASSWORD = input('Enter your password: ')

USER_POOL_ID = "us-east-2_D8EPsTtjX"
APP_CLIENT_ID = "7gar0jcbchb5v6jbns0ncpjd6f"

def set_tokens(tokens):
    with open("tokens.txt", "w") as f:
        f.write(json.dumps(tokens))

def init_auth_user_password(username, password):
    # Log in the user we just created

    client = boto3.client("cognito-idp")

    # This is less secure, but simpler
    response = client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": username, "PASSWORD": password},
        ClientId=APP_CLIENT_ID,
    )
    print("----- Log in response -----")
    pprint(response)
    print("---------------------------")

    # AWS official docs on using tokens with user pools:
    # https://amzn.to/2HbmJG6
    # If authentication was successful we got three tokens
    jwt_access = response["AuthenticationResult"]["AccessToken"]
    jwt_id = response["AuthenticationResult"]["IdToken"]
    jwt_refresh = response["AuthenticationResult"]["RefreshToken"]

    print("Log in success")
    return jwt_access, jwt_id, jwt_refresh

def main():
    jwt_access, jwt_id, jwt_refresh = init_auth_user_password(USERNAME, PASSWORD)
    set_tokens({"access": jwt_access, "id": jwt_id, "refresh": jwt_refresh})

main()