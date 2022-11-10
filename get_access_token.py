import aiohttp
import asyncio
import time
import pprint
import jwt
import os
import dotenv
import json

pp = pprint.PrettyPrinter(indent=4)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)
 
async def create_private_key_jwt():
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

async def main():
	okta_url = os.environ.get('OKTA_URL')
	private_key_jwt = await create_private_key_jwt()
	scope = os.environ.get('SCOPES')
 
	data = f'grant_type=client_credentials&scope={scope}&client_assertion_type=urn%3Aietf%3Aparams%3Aoauth%3Aclient-assertion-type%3Ajwt-bearer&client_assertion={private_key_jwt}'
	headers = {
		'Accept': 'application/json',
		'Content-Type': 'application/x-www-form-urlencoded'
	}
 
	async with aiohttp.ClientSession() as session:
		async with session.post(okta_url + '/oauth2/v1/token',
							data=data, headers=headers) as resp:
			res = await resp.json()

	print('\n///////////////// Access Token:\n')
	pp.pprint(res)

asyncio.run(main())