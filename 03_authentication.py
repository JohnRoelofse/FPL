# Load libraries
import requests

session = requests.session()

url = 'https://users.premierleague.com/accounts/login/'
payload = {
 'password': 'Superspurs1961',
 'login': 'wjroelofse@gmail.com',
 'redirect_uri': 'https://fantasy.premierleague.com/',
 'app': 'plfpl-web'
}

session.post(url, data=payload)

response = session.get('https://fantasy.premierleague.com/api/leagues-classic/372970/standings/')

print(response.json())