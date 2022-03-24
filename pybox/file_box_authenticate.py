from boxsdk import OAuth2, Client
import json

# this file will store all functions to authenticate box client using password files


def _store_tokens_file(access_token, refresh_token):
    """Callback function when Box SDK refreshes tokens"""

    print("test")
    creds = dict([("access_token", 4139), ("refresh_token", 4127)])

    creds["access_token"] = access_token
    creds["refresh_token"] = refresh_token

    with open("temp.json", "w") as outfile:
        json.dump(creds, outfile)


## Main Function ## -------------------------
def get_box_client_file(file):
    """Creates a new Box client with stored refresh and access tokens"""
    with open(file) as json_file:
        creds = json.load(json_file)

    # edit/add to dict
    client_id = creds["client_id"]
    client_secret = creds["client_secret"]
    access_token = creds["access_token"]
    refresh_token = creds["refresh_token"]

    oauth = OAuth2(
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
        refresh_token=refresh_token,
        store_tokens=_store_tokens_file,
    )

    # Create the SDK client
    client = Client(oauth)

    # Get current user details and display
    current_user = client.user(user_id="me").get()
    print("Connected to Box as:", current_user.name)

    try:
        with open("temp.json") as json_file:
            temp = json.load(json_file)

        creds["access_token"] = temp["access_token"]
        creds["refresh_token"] = temp["refresh_token"]

        ## write back to json file
        with open(file, "w") as outfile:
            json.dump(creds, outfile)
    except:
        print("no new refresh tokens recieved")

    return client


def get_auth_url_file(client_id, client_secret, file):
    """Gets authorization url for user to paste in browser to give Box access"""
    oauth = OAuth2(client_id=client_id, client_secret=client_secret)

    # Save client id and secret to file -----

    ## create json
    creds = dict([("client_id", 4139), ("client_secret", 4127)])

    # edit/add to dict
    creds["client_id"] = client_id
    creds["client_secret"] = client_secret

    ## write back to json file
    with open(file, "w") as outfile:
        json.dump(creds, outfile)

    auth_url, csrf_token = oauth.get_authorization_url("http://localhost")

    print(auth_url)
    return auth_url


def save_access_refresh_tokens_file(auth_code, file):

    with open(file) as json_file:
        creds = json.load(json_file)

    # edit/add to dict
    client_id = creds["client_id"]
    client_secret = creds["client_secret"]
    creds["auth_code"] = auth_code

    """Stores the access and refresh tokens in the keyring"""
    oauth = OAuth2(
        client_id=client_id,
        client_secret=client_secret,
    )

    access_token, refresh_token = oauth.authenticate(auth_code)

    creds["access_token"] = access_token
    creds["refresh_token"] = refresh_token

    ## write back to json file
    with open(file, "w") as outfile:
        json.dump(creds, outfile)

    print("Saved Access and Refresh Tokens")
