import requests
import os
import dotenv


dotenv.load_dotenv()
token_api_url = os.getenv('PANCAKESWAP_API')
username = os.getenv('API_USERNAME')
password = os.getenv('API_PASSWORD')
base = os.getenv('API_BASE')
access_token = os.getenv('API_ACCESS_TOKEN','')
refresh_token = os.getenv('API_REFRESH_TOKEN','')


def login_api():
    '''Login user using saved credentials.'''
    global access_token, refresh_token

    r = requests.post(base+'auth/login',
                      json={
                          'username':username,
                          'password':password
                      })
    
    r= r.json()
    access_token = r['user']['access']
    refresh_token = r['user']['refresh']
    
    set_token_env(access_token,refresh_token)
    
    return r


def check_login():
    '''Check if user is already logged in using saved access token.'''
    global access_token,refresh_token

    r = requests.get(base+'auth/me',
                     headers={
                         'Authorization':'Bearer '+access_token
                     })
    
    if r or r.status_code == 200:
        res = r.json()
        
    elif r.status_code == 401:
        r2 = requests.post(base+'auth/token/refresh',
                     headers={
                         'Authorization':'Bearer '+refresh_token
                     })
        res = r2.json()
        set_token_env(res['access'],refresh_token)
        
    else:
        res = login_api()
        
    return res


def set_token_env(access_token, refresh_token):
    '''Saves the access and refresh token in the .env file'''
    dotenv.set_key('.env','API_ACCESS_TOKEN',access_token)
    dotenv.set_key('.env','API_REFRESH_TOKEN',refresh_token)


def get_quotes():
    '''Get all available tokens'''
    res = check_login()
    
    if 'access' in res['user']:
        access = res['user']['access']
    
    else:
        global access_token
        access = access_token
        
    r = requests.get(base+'token/all',
                     headers={
                         'Authorization':'Bearer '+access
                    }).json()
    data = r['data']
    
    quotes = []
    
    for token in data:
        quote = requests.get(token_api_url+token['contract']).json()
        if not 'error' in quote:
            quotes.append([quote['data']['symbol'],quote['data']['price']])
        else:
            quotes.append(['none','none'])
        
    return quotes