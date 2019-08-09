# Load libraries
import ssl
import urllib.request, urllib.parse, urllib.error
import json
import sqlite3

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Provide authentication


# Specify url and parameters 
url = 'https://fantasy.premierleague.com/api/leagues-classic/372970/standings/'

# Retrieve data from url
uh = urllib.request.urlopen(url, context=ctx)
data = uh.read().decode()

# Deserialise (decode) JSON to Python objects
js = json.loads(data)

# Extract Entries from JSON
entries = js['new_entries']

### Store data in fpl sqlite3 database

# Connect to database
conn = sqlite3.connect('fpl.sqlite')
cur = conn.cursor()

# Events 
for item in entries:
    cur.execute("INSERT INTO league (entry_id, entry_name, player_first_name, player_second_name) VALUES ( ?, ?, ?, ? )", 
                    (item['entry'], item['entry_name'], item['player_first_name'], item['player_second_name']))

# Commit changes
conn.commit()

# Close connection
conn.close()