import boto3
import json
from pprint import pprint
#from aws_srp import AWSSRP
from botocore.exceptions import ClientError

USERNAME = input('Type in your desired username: ')
PASSWORD = input('Type in a minimum 6 character password (letters and numbers only): ')
EMAIL = input('Type in your email: ')

USER_POOL_ID = "us-east-2_D8EPsTtjX"
APP_CLIENT_ID = "7gar0jcbchb5v6jbns0ncpjd6f"

def sign_up(username, password, email):
    client = boto3.client("cognito-idp")

    try:
        # Add user to pool
        sign_up_response = client.sign_up(
            ClientId=APP_CLIENT_ID,
            Username=username,
            Password=password,
            UserAttributes=[{"Name": "email", "Value": email}, {"Name": "custom:allowed_access", "Value": "1111111"}],
        )
        pprint(sign_up_response)
    except ClientError as err:
        # Probably user already exists
        print(err)


def confirm_sign_up(username, code):
    client = boto3.client("cognito-idp")

    response = client.confirm_sign_up(ClientId=APP_CLIENT_ID, Username=username, ConfirmationCode=code)

    pprint(response)
    print("User confirmed.")

def main():
    sign_up(USERNAME, PASSWORD, EMAIL)

    code = input("Check your email...Please enter verification code:")
    confirm_sign_up(USERNAME, code)


main()