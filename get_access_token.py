
import time
import pprint
import jwt
import os
import dotenv
import json
import http.client

pp = pprint.PrettyPrinter(indent=4)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)
 
def create_private_key_jwt():
	client_id = os.environ.get('CLIENT_ID')
	okta_url = os.environ.get('OKTA_URL')
	okta_token_endpoint = f'{okta_url}/oauth2/v1/token'
	private_key = os.environ.get('PRIVATE_KEY')
	token = jwt.encode({
		'iss': client_id,
		'sub': client_id,
		'aud': okta_token_endpoint,
		"exp": int(time.time()) + 3600
	},
	private_key,
	algorithm='RS256',
	)
	return token

def main():
	okta_url = os.environ.get('OKTA_URL')
	private_key_jwt = create_private_key_jwt()
	scope = os.environ.get('SCOPES')
 
	payload = f'grant_type=client_credentials&scope={scope}&client_assertion_type=urn%3Aietf%3Aparams%3Aoauth%3Aclient-assertion-type%3Ajwt-bearer&client_assertion={private_key_jwt}'

	headers = {
		'Accept': 'application/json',
		'Content-Type': 'application/x-www-form-urlencoded'
	}

	conn = http.client.HTTPSConnection(okta_url.replace('https://', ''))

	conn.request(
		'POST',
		f'/oauth2/v1/token',
		payload,
		headers
		)

	response = conn.getresponse()
	print(f"code:{response.status}\nrespoonse:{json.loads(response.read())['access_token']}")
 
main()