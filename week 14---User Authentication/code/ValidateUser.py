import jwt
import json
from pprint import pprint

USER_POOL_ID = "us-east-2_D8EPsTtjX"
APP_CLIENT_ID = "7gar0jcbchb5v6jbns0ncpjd6f"

REGION = "us-east-2"
PUBLIC_KEY_URL = "https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json".format(REGION, USER_POOL_ID)

def get_tokens():
    with open("tokens.txt", "r") as f:
        return json.loads(f.read())

def get_public_key(token):
    jwk = jwt.PyJWKClient(PUBLIC_KEY_URL)
    key_obj = jwk.get_signing_key_from_jwt(token)
    return key_obj.key

def validate_id_token(token, public_key):

    try:
        data = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=APP_CLIENT_ID,
            options={"verify_exp": True, "verify_signature": True, "verify_aud": True},
        )
        pprint(data)
        print("Access to server resources granted")
        return data["custom:allowed_access"]
    except Exception as e:
        print('Access to server resources denied:"{}"'.format(e))

def main():

    tokens = get_tokens()
    public_key = get_public_key(tokens["id"])
    validate_id_token(tokens["id"], public_key)

main()
