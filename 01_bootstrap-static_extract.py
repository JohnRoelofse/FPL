# Load libraries
import ssl
import urllib.request, urllib.parse, urllib.error
import json
import sqlite3

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Specify url and parameters 
url = 'https://fantasy.premierleague.com/api/bootstrap-static/'

# Retrieve data from url
uh = urllib.request.urlopen(url, context=ctx)
data = uh.read().decode()

# Deserialise (decode) JSON to Python objects
js = json.loads(data)

# Extract event, team and player data from JSON
events = js['events']
teams = js['teams']
players = js['elements']    # players referred to as elements

### Store data in fpl sqlite3 database

# Connect to database
conn = sqlite3.connect('fpl.sqlite')
cur = conn.cursor()

# Events 
for item in events:
    cur.execute("INSERT INTO events (gameweek_id, name, deadline_time) VALUES ( ?, ?, ? )", 
                    (item['id'], item['name'], item['deadline_time']))

# Teams
for item in teams:
    cur.execute("INSERT INTO teams (team_id, name, short_name) VALUES ( ?, ?, ? )", 
                    (item['id'], item['name'], item['short_name']))

# Players
for item in players:
    cur.execute("INSERT INTO players (player_id, team_id, first_name, second_name) VALUES ( ?, ?, ? , ? )", 
                    (item['id'], item['team'], item['first_name'], item['second_name']))

# Commit changes
conn.commit()

# Close connection
conn.close()