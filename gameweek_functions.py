def check_gameweek():
    """
    This function checks what the current gameweek is and returns that value as an integer.

    This is done by:
        - Extracting a list of the gameweeks and their start times from the events table
        - Converting the start time to a datetime.datetime object
        - Comparing the gameweek start times to the time now

    Notes:
        - The gameweek start time is stored in the events table as a string but is in UTC format
    """

    import sqlite3
    from datetime import datetime

    # Make a connection to the fpl database
    conn = sqlite3.connect('fpl.sqlite')
    cur = conn.cursor()

    # Extract list of gameweeks and the gameweek start time 
    gameweek_time_start_list = cur.execute("select gameweek_id, deadline_time from events").fetchall()

    # Close connection
    conn.close()

    # Create dictionary
    gameweek_time_start_dict = dict()
    for row in gameweek_time_start_list:
        gameweek_time_start_dict[row[0]] = datetime.strptime(row[1], '%Y-%m-%dT%H:%M:%SZ')

    # Check what gameweek it is and return the value as an integer
    utcnow = datetime.utcnow()
    for gameweek in gameweek_time_start_dict:
        if gameweek == 1:
            if utcnow < gameweek_time_start_dict[gameweek]:
                return gameweek
            elif utcnow > gameweek_time_start_dict[gameweek] and utcnow < gameweek_time_start_dict[gameweek+1]:
                return gameweek
        elif utcnow > gameweek_time_start_dict[gameweek] and utcnow < gameweek_time_start_dict[gameweek+1]:
            return gameweek
        elif gameweek == 38:
            return 38

def gameweek_captains():
    import sqlite3

    # Open connection to database
    conn = sqlite3.connect('fpl.sqlite')
    cur = conn.cursor()

    # Specify gameweek
    gameweek = check_gameweek()

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

    # Store data in dictionary
    data = dict()
    for row in most_captained:
        data[row[0]] = str(round(row[1]*100, 2)) + '%'

    # Close connection
    conn.close()

    # Return data
    return data