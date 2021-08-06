from boxsdk import OAuth2, Client
import keyring

## Helper functions ## ---------------------
def _read_tokens():
    """Reads authorisation tokens from keyring"""
    # Use keyring to read the tokens
    access_token = keyring.get_password('Box_Auth', 'niranjan.ilawe@box.com')
    refresh_token = keyring.get_password('Box_Refresh', 'niranjan.ilawe@box.com')
    return access_token, refresh_token


def _store_tokens(access_token, refresh_token):
    """Callback function when Box SDK refreshes tokens"""
    # Use keyring to store the tokens
    keyring.set_password('Box_Auth', 'niranjan.ilawe@box.com', access_token)
    keyring.set_password('Box_Refresh', 'niranjan.ilawe@box.com', refresh_token)

## Main Function ## -------------------------
def get_box_client():
    """Creates a new Box client with stored refresh and access tokens"""
    access_token, refresh_token = _read_tokens()
    client_id = keyring.get_password('Box_client_id', 'niranjan.ilawe@box.com')
    client_secret = keyring.get_password('Box_client_secret', 'niranjan.ilawe@box.com')

    oauth = OAuth2(
        client_id=client_id,
        client_secret=client_secret,
        access_token=access_token,
        refresh_token=refresh_token,
        store_tokens=_store_tokens,
    )
    
    # Create the SDK client
    client = Client(oauth)
    
    # Get current user details and display
    current_user = client.user(user_id='me').get()
    print('Connected to Box as:', current_user.name)

    return(client)

def get_auth_url(client_id, client_secret):
    """Gets authorization url for user to paste in browser give Box access"""
    oauth = OAuth2(
        client_id=client_id,
        client_secret=client_secret
    )
    
    # Save client id and secret
    keyring.set_password('Box_client_id', 'niranjan.ilawe@box.com', client_id)
    keyring.set_password('Box_client_secret', 'niranjan.ilawe@box.com', client_secret)

    auth_url, csrf_token = oauth.get_authorization_url('http://localhost')

    print(auth_url)
    return(auth_url)

def save_access_refresh_tokens(auth_code):

    client_id = keyring.get_password('Box_client_id', 'niranjan.ilawe@box.com')
    client_secret = keyring.get_password('Box_client_secret', 'niranjan.ilawe@box.com')

    """Stores the access and refresh tokens in the keyring"""
    oauth = OAuth2(
        client_id=client_id,
        client_secret=client_secret,
    )
    
    access_token, refresh_token = oauth.authenticate(auth_code)
    keyring.set_password('Box_Auth', 'niranjan.ilawe@box.com', access_token)
    keyring.set_password('Box_Refresh', 'niranjan.ilawe@box.com', refresh_token)
    print('Saved Access and Refresh Tokens')