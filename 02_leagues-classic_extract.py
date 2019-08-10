# Load libraries
import sqlite3
from authentication import authenticate

# Start authenticated session
session = authenticate()

# Specify url
url = 'https://fantasy.premierleague.com/api/leagues-classic/372970/standings/'

# Retrieve data from url
get_request = session.get(url)

# Deserialise (decode) JSON to Python objects
js = get_request.json()

# Extract dictionary containing entry IDs
league = js['standings']['results']

### Store data in fpl sqlite3 database

# Connect to database
conn = sqlite3.connect('fpl.sqlite')
cur = conn.cursor()

# Insert  
for item in league:
    cur.execute("INSERT INTO league (entry_id, entry_name, player_name) VALUES ( ?, ?, ? )", 
                    (item['entry'], item['entry_name'], item['player_name']))

# Commit changes
conn.commit()

# Close connection
conn.close()