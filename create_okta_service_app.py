import aiohttp
import asyncio
import pprint
import os
import dotenv
import json

pp = pprint.PrettyPrinter(indent=4)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)
 
async def main():
	okta_url = os.environ.get('OKTA_URL')
	modulus = os.environ.get('MODULUS')
	api_key = os.environ.get('API_KEY')
 
	print("Enter a name for your application:")
	app_name = input()

	# conn = http.client.HTTPSConnection(okta_url[8:])
	payload = {
		'client_name': app_name or 'Private Key JWT Service App',
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
	async with aiohttp.ClientSession() as session:
		async with session.post(okta_url + '/oauth2/v1/clients',
                         json=payload, headers=headers) as resp:
			res = await resp.json()

	print('\n///////////////// Okta Service app created: \n \n')
	pp.pprint(res)

	client_id = res['client_id']

	print(f'\n///////////////// Setting CLIENT_ID in .env: {client_id}')
	dotenv.set_key(dotenv_path, 'CLIENT_ID', client_id)

	scopes = os.environ.get('SCOPES').split()

	for scope in scopes:
		await grant_scopes_in_service_app(okta_url, api_key, client_id, scope)

async def grant_scopes_in_service_app(okta_url, api_key, client_id, scope):
	payload = {
		'issuer': okta_url,
		'scopeId': scope
	}
	headers = {
		'Accept': 'application/json',
		'Content-Type': 'application/json',
		'Authorization': f'SSWS {api_key}'
	}

	async with aiohttp.ClientSession() as session:
		async with session.post(okta_url + f'/api/v1/apps/{client_id}/grants',
                         json=payload, headers=headers) as resp:
			res = await resp.json()

	print('\n///////////////// Scopes granted:\n')
	pp.pprint(res)

asyncio.run(main())