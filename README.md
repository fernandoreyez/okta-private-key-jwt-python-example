# Private Key JWT OAuth Flow (Python)

This repo aims to simplify the process of creating a public/private key pair, using the public key to create an application at the identity provider and using the private key to sign JWTs to obtain access tokens from said IdP. At time of writing, this is written for integrating with Okta but I would like to add more IdPs over time.

## Dependencies:

- [virtualenv](https://docs.python.org/3/library/venv.html)

## Setup
1. Clone the repo, open terminal and ```cd``` into the project root.
2. Create a new virtualenv in the root folder with ```virtualenv env```
3. Run the virtual environment with ```source env/bin/activate```
4. Install necessary Python packages with ```pip install -r requirements.txt```
5. In the root folder, create a new .env file and paste the following values into it:

```
PRIVATE_KEY=
PUBLIC_KEY=
MODULUS=
CLIENT_ID=
OKTA_URL=
API_KEY=
SCOPES=
```
Scripts will generate values for the first 4 vars. You will need to fill out the other values. **Note:** the API key is needed for creating the OAuth client in Okta, so make sure the token you use has permissions to create applications.

- OKTA_URL=https://{your_okta_domain}
- API_KEY={okta_api_key}
- SCOPES='okta.users.read okta.users.manage'

*The SCOPES var is an string of scopes (seperated by spaces) granted to your eventual access token that you will be using for management tasks. I put in a couple common ones as a placeholder. In your Okta application, it would look like this:*

![SCOPES_1](https://i.imgur.com/B4zNpom.png)

## Running the Scripts

To run these scripts, make sure you are still in the root folder of the cloned repository.

### Generate Keypair

In the Private Key JWT flow, the first step you need to take is generating a public/private keypair. The public key is shared with the identity provider to verify the JWT signed with your private key. To generate the keys, type the following command into the terminal:

```
python generate_keys.py
```

You should see confirmation printed to the terminal:

```
///////////////// Keys generated and added to .env file.
```

Sure enough, you can pop over to the .env file to see the values populated there.

### Create OAuth Service App in Okta

Now that you have the keypair, you can create the OAuth app in Okta with the public key. The scopes you defined above will also be granted in the application. Type the following into the terminal:

```
python create_okta_service_app.py
```

You will get confirmation in the terminal of the created app, that the client ID of the app was updated in your .env file, as well as scopes granted.

```
///////////////// Okta Service app created: 

{application object}

///////////////// Setting CLIENT_ID in .env:

{client ID of newly created app}

///////////////// Scopes granted: 

{scopes granted to the application}
```

If you navigate to your applications in Okta, you will see this newly created app under the name **Private Key JWT Service App**.

### Get Access Token

The above two scripts should only need to be ran once for setup. From hereon out, you can run the following command to get an access token from Okta:

```
python get_access_token.py
```

You should see the access token printed to terminal:

```
///////////////// Access Token:

{access_token}
```

You can now use this token to perform management tasks on your Okta org based on your defined scopes by passing it in the **Authorization** header as **Bearer {access_token}**.