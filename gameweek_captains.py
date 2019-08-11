import sqlite3

# Open connection to database
conn = sqlite3.connect('fpl.sqlite')
cur = conn.cursor()

# Specify gameweek
gameweek = 1

# Work out gameweek captain picks
most_captained = cur.execute(f"""
select b.second_name, count(*)/cast(38 as float) as percentage
from gameweek_picks as a
left join players as b
    on a.player_id = b.player_id
where gameweek_id = {gameweek} and is_captain = 1
group by 1 
order by 2 desc
""").fetchall()

for row in most_captained:
    print(row[0], str(round(row[1]*100, 2)) + '%')

# Close connection
conn.close()