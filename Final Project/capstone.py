import logging
import requests
import io
import boto3
from botocore.exceptions import ClientError
import json
from pprint import pprint

def create_bucket(bucket_name, region):

    try:
        s3_client = boto3.client('s3', region_name=region)
        location = {'LocationConstraint': region}
        s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    
    print('Bucket created successfully')
    return True

def list_all_buckets():
    
    try:
        s3_client = boto3.client('s3')
        response = s3_client.list_buckets()
    except ClientError as e:
        logging.error(e)
        return False

    # Output the bucket names
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')
    
    return True

# Put something in an S3 bucket.
def upload_file(bucket_name, file_name, object_name):

    try:
        s3_client = boto3.client('s3')
        s3_client.upload_file(file_name, bucket_name, object_name)
    except ClientError as e:
        logging.error(e)
        return False

    print('File uploaded successfully')
    return True

# List the contents of an S3 bucket
def list_all_objects(bucket_name):

    try:
        s3_client = boto3.client('s3')
        paginator = s3_client.get_paginator("list_objects_v2")

        for page in paginator.paginate(Bucket=bucket_name):

            for content in page["Contents"]:
                key = content['Key']    
                print(key)

    except ClientError as e:
        logging.error(e)
        return False

    return True

# Read something from a DynamoDB table 

def get_item(pk,sk):

    try:
        db_client = boto3.client('dynamodb')
        response = db_client.get_item(
        Key={
            'pk': {
            'S': pk,
            },
            'sk': {
            'S': sk,
            },      
        },
        TableName='Capstone',
        )
        print(response["Item"])
        return response["Item"]
    except ClientError as e:
        logging.error(e)
        return None

# Write something to a DynamoDB table.
def put_item(pk,sk,vendor,title,description,PrimaryUnits,PrimaryUnitsPerBottle,DoseUnit,DosePerPrimaryUnit,PriceUnits,price,CountrySold):

    try:
        db_client = boto3.client('dynamodb')
        db_client.put_item(
        Item={
            'pk': {
            'S': pk,
            },
            'sk': {
            'S': sk,
            },
            'vendor': {
            'S': vendor,
            },
            'title': {
            'S': title,
            },
            'description': {
            'S': description,
            },
            'price': {
            'N': str(price), #Note: Even though a number, it is passed as a string
            },
            'PrimaryUnits':{
            'S': PrimaryUnits,
            },
            'PrimaryUnitsPerBottle':{
            'S': PrimaryUnitsPerBottle
            },
            'DoseUnit':{
            'S': DoseUnit
            },
            'DosePerPrimaryUnit':{
            'S': DosePerPrimaryUnit
            },
            'Price Units':{
            'S': PriceUnits
            },
            'Price':{
            'S':price
            },
            'Country Sold in':{
            'S':CountrySold 
            },

        },
        ReturnConsumedCapacity='TOTAL',
        TableName=TABLE_NAME,
        )
        return True
    except Exception as e:
        logging.error(e)
        return False

# Create user in Cognito
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
# Login user in Cognito
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

# Delete user in Cognito
def delete(jwt_access):
    client = boto3.client("cognito-idp")
    delete=client.delete_user(
        AccessToken=jwt_access
        )

def main():

    # sql_espression = """SELECT * FROM S3Object"""
    TABLE_NAME="capstone"
    sql_espression = """SELECT s.Title FROM S3Object s"""
    #Define quit parameter which will terminate the program upon user entering string "Q"
    quit=""
    #While loop that keeps running as long as user inputs something other than "Q"
    while quit!="Q":
    #Print out welcome screen and list options for user to select
        print("Welcome to Amazon S3!")
        print("What would you like to do?")
        print("A. Create a bucket")
        print("B. List all available buckets")
        print("C. Upload a file to a bucket")
        print("D. List contents of a chosen bucket")
        print("E. Create an account with us")
        print("F. Login to your account")
        print("G. Delete your account (PLEASE LOGIN TO YOUR ACCOUNT FIRST)")
        print("H. Read data from a DynamoDB Table (CapStone Table only)")
        print("I. Write data to a DynamoDB Table")
        val=input("Please select what you would like to do A-I: ")
    #If else logic that processes user inputs
        if val=="A" or val=="a":
            #Prompts user for bucket name and region and calls function to create bucket
            bucket_name=input("Please type in a unique bucket name: ")
            region=input("Please type in the appropriate AWS region: ")
            create_bucket(bucket_name,region)
        elif val=="B" or val=="b":
            #Lists all buckets
            list_all_buckets()
        elif val=="C" or val=="c":
            #Prompts user for bucket name and file name they would like to upload into that bucket. Calls function to upload the file
            bucket_name=input("Please type in the bucket name you would like to upload the file to: ")
            upload_file_name=input("Please type in the name of the file you would like to upload: ")
            upload_file(bucket_name, upload_file_name, upload_file_name)
        elif val=="D" or val=="d":
            #Prompts user for bucket name of files they would like to see. Calls functions to list all objects inside bucket
            bucket_name=input("Please type in the name of the bucket which you would like to see all files: ")
            list_all_objects(bucket_name)
        elif val=="E" or val=="e":
            #Prompts for a username, password and email
            USERNAME = input('Type in your desired username: ')
            PASSWORD = input('Type in a minimum 6 character password (letters and numbers only): ')
            EMAIL = input('Type in your email: ')
            sign_up(USERNAME, PASSWORD, EMAIL)
            code = input("Check your email...Please enter verification code:")
            confirm_sign_up(USERNAME, code)
        elif val=="F" or val=="f":
            #Prompots user to enter username and password and logs them in
            USERNAME = input('Enter your username: ')
            PASSWORD = input('Enter your password: ')
            jwt_access, jwt_id, jwt_refresh = init_auth_user_password(USERNAME, PASSWORD)
            set_tokens({"access": jwt_access, "id": jwt_id, "refresh": jwt_refresh})
        elif val=="G" or val=="g":
            delete(jwt_access)
        elif val=="H" or val=="h":
            pk=input("Enter the pk of the item you would like to get: ")
            sk=input("Enter the sk of the item you would like to get: ")
            get_item(pk,sk)
        elif val=="I" or val=="i":
            TABLE_NAME="Capstone"
            item=input("Input the data of a vitamin product you would like to add to the database in the following format: (pk,sk,vendor,title,description,PrimaryUnits,PrimaryUnitsPerBottle,DoseUnit,DosePerPrimaryUnit,PriceUnits,price,CountrySold) ")
            put_item(item)
            print(item)
        else:
            #Final call, asks user to rerun file to try again
            quit=input("Wrong answer, rerun file to try again")
        quit=input("Press Q to quit or any other key to continue")


main()