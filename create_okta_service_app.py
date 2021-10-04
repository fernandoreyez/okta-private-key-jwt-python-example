import http.client
import pprint
import os
import dotenv
import json

pp = pprint.PrettyPrinter(indent=4)

def create_okta_service_app(env_path):
	okta_url = os.environ.get('OKTA_URL')
	modulus = os.environ.get('MODULUS')
	api_key = os.environ.get('API_KEY')

	conn = http.client.HTTPSConnection(okta_url[8:])
	payload = {
		'client_name': 'Private Key JWT Service App',
		'response_types': [
			'token'
		],
		'grant_types': [
			'client_credentials'
		],
		'token_endpoint_auth_method': 'private_key_jwt',
		'application_type': 'service',
		'jwks': {
			'keys': [
				{
					'kty': 'RSA',
					'e': 'AQAB',
					'use': 'sig',
					'kid': 'O4O',
					'alg': 'RS256',
					'n': modulus
				}
			]
		} 
	}
	headers = {
		'Accept': 'application/json',
		'Content-Type': 'application/json',
		'Authorization': f'SSWS {api_key}'
	}
	conn.request('POST', '/oauth2/v1/clients', json.dumps(payload), headers)
	res = conn.getresponse()
	data = res.read()

	print('\n///////////////// Okta Service app created: \n \n')
	pp.pprint(json.loads(data))

	client_id = json.loads(data)['client_id']
	print(f'\n///////////////// Setting CLIENT_ID in .env:\n \n{client_id}')
	dotenv.set_key(env_path, 'CLIENT_ID', client_id)

	grant_scopes_in_service_app(okta_url, api_key, client_id)

def grant_scopes_in_service_app(okta_url, api_key, client_id):
	scope = os.environ.get('SCOPES')
	conn = http.client.HTTPSConnection(okta_url[8:])
	payload = {
		'issuer': okta_url,
		'scopeId': scope
	}
	headers = {
		'Accept': 'application/json',
		'Content-Type': 'application/json',
		'Authorization': f'SSWS {api_key}'
	}
	conn.request('POST', f'/api/v1/apps/{client_id}/grants', json.dumps(payload), headers)
	res = conn.getresponse()
	data = res.read()

	print('\n///////////////// Scopes granted: \n \n')
	pp.pprint(json.loads(data))

if __name__ == '__main__':
	dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
	dotenv.load_dotenv(dotenv_path)
	create_okta_service_app(dotenv_path)