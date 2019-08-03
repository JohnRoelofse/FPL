import sqlite3

# Create database connection
conn = sqlite3.connect('fpl.sqlite')
cur = conn.cursor()

# Drop tables if they exist
cur.execute("DROP TABLE IF EXISTS players")
cur.execute("DROP TABLE IF EXISTS teams")
cur.execute("DROP TABLE IF EXISTS events")

# Create player table
cur.execute("""
CREATE TABLE players (
    player_id INTEGER, 
    team_id INTEGER,
    first_name TEXT, 
    second_name TEXT
    )
""")

# Create teams table
cur.execute("""
CREATE TABLE teams (
    team_id INTEGER,
    name TEXT,
    short_name TEXT
)
""")

# Creat events table
cur.execute("""
CREATE TABLE events (
    gameweek_id INTEGER,
    name TEXT,
    deadline_time TEXT
)
""")

cur.close()