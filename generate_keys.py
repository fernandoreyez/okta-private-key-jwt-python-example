import asyncio
import os
import codecs
import dotenv
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(dotenv_path)

async def main():
	key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, key_size=2048)

	public_key = key.public_key().public_bytes(serialization.Encoding.OpenSSH, serialization.PublicFormat.OpenSSH)

	pem = key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption())

	private_key_str = pem.decode('utf-8')
	public_key_str = public_key.decode('utf-8')
	modulus = codecs.encode(codecs.decode(hex(key.public_key().public_numbers().n)[2:], 'hex'), 'base64').decode()

	dotenv.set_key(dotenv_path, 'PRIVATE_KEY', private_key_str)
	dotenv.set_key(dotenv_path, 'PUBLIC_KEY', public_key_str)
	dotenv.set_key(dotenv_path, 'MODULUS', modulus)

	print('\n///////////////// Keys generated and added to .env file.\n')

asyncio.run(main())