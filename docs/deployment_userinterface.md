# Deployment of User Interface
This section provides information regarding the deployment of the BrainKB UI, both in the development and the production mode.

## System Requirements
- The BrainKB UI is based on NextJS; we need to install the Node.js. When writing this document, the minimum version is **Node.js 18.17 or later**. For more (or latest) information, please check NextJS website.

	- [https://nextjs.org/docs/getting-started/installation](https://nextjs.org/docs/getting-started/installation)

- Once all the NextJS requirements has been met or covered, next step is to configure the OAuth. In our case we use Google and GitHub. Therefore, you would need to obtain the OAuth client ID and secret and update the ```.env``` file (shown below). Additionally, you also need to provide the secret for [NextAuth](https://next-auth.js.org/), a library that we use authentication. The ```NEXTAUTH_URL``` for development is ```http://localhost:3000```. Similarly, the GitHub secret and client ID can be obtained from GitHub at [https://github.com/settings/tokens](https://github.com/settings/tokens) and Google at [https://console.cloud.google.com/](https://console.cloud.google.com/).

	```
	#OAuth credentials
	GITHUB_CLIENT_ID= 
	GITHUB_CLIENT_SECRET=

	GOOGLE_CLIENT_ID=
	GOOGLE_CLIENT_SECRET=

	#Auth Config
	NEXTAUTH_SECRET= 
	NEXTAUTH_URL=
	````
	
	**<span style="color: red;">Note:</span>** For Google OAuth, unless the ```Publishing status``` is ```published```, it will be ```Testing``` as shown in {numref}`google_oauth_setup`. Since this is in a testing mode, only the testing users can log in via Google OAuth. 

	If the ```User type``` is ```Internal```, only the organizational members can log in (e.g., *.mit.edu).

	```{figure} oauth_setup_google.png
	:name: google_oauth_setup
	Google OAuth setup.
	```

## Running in Non-Containerized Development Mode
You can run the application either using ```npm``` or ```next``` command as follows.

- Using ```npm```
	```npm run dev```

- Using ```next```
	```next dev```

## Running in Non-Containerized Production Mode
To run in a production mode first you need to build the application and start. Run the following command in order.
- ```next build```
- ```next start```


## Running in Containerized Mode

## Known Issues

Especially with the Google based authentication, even after successful setup, you might get error regarding mismatch redirect URI, as shown in {numref}`google_oauth_error`, thereby preventing you to log in. This is because unlike GitHub-based OAuth, where you can redirect to the pages that one desire, e.g., home page, the redirect URI in case of Google needs to be specific.

```{figure} error_oauth_google.png
:name: google_oauth_error
Unable to login with Google.
```

To fix this issue, set the redirect URI as ```https://{YOUR_DOMAIN}/api/auth/callback/google```. In ```YOUR_DOMAIN``` is:
- ```https://localhost:3000/api/auth/callback/google``` development mode
- in production, replace ```YOUR_DOMAIN``` with registered domain name

More information regarding these callbacks can be obtained from NextJS website at 
[https://next-auth.js.org/providers](https://next-auth.js.org/providers).


	