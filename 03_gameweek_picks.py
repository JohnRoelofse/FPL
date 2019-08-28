# Load required modules
from authentication import authenticate
from gameweek_functions import check_gameweek
import requests
import sqlite3

# Open authenticated session
session = authenticate()

# Connect to SQLite database
conn = sqlite3.connect('fpl.sqlite')
conn.row_factory = lambda cursor, row: row[0]
cur = conn.cursor()

# Get list of fpl players from league table
fpl_players = cur.execute('select entry_id from league').fetchall()

# Get gameweek
gameweek = check_gameweek()

# Loop through all fpl players to get their picks for the week
gameweek_picks = dict()
for player in fpl_players:
    try:
        get_request = session.get(f'https://fantasy.premierleague.com/api/entry/{player}/event/{gameweek}/picks/')
        js = get_request.json()
        gameweek_picks[player] = js['picks']
    except:
        continue
    
# Insert gameweek picks into gameweek_picks table
for fpl_player in gameweek_picks:
    for item in gameweek_picks[fpl_player]:
        cur.execute("""INSERT INTO gameweek_picks (gameweek_id, 
                                                    entry_id,
                                                    player_id,
                                                    position,
                                                    is_captain,
                                                    is_vice_captain
                                                    ) VALUES (?, ?, ?, ?, ?, ?) """,
                    (gameweek, fpl_player, item['element'], item['position'], item['is_captain'], item['is_vice_captain']))

# Commit changes
conn.commit()

# Close connection
conn.close()