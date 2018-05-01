#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    delete_matches_query = "DELETE FROM Matches_Tbl;"
    c.execute(delete_matches_query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    delete_players_query = "DELETE FROM Players_Tbl;"
    c.execute(delete_players_query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    count_players_query = "SELECT count(id) AS player_count FROM Players_Tbl;"
    c.execute(count_players_query)
    player_count = c.fetchall()
    db.close()
    return player_count[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO Players_Tbl (name) VALUES (%s)", (name,))
    db.commit()
    db.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    display_standing_query = "SELECT id, name, number_wins, number_game FROM Standings_Vw ORDER BY number_wins DESC;"
    c.execute(display_standing_query)
    player_standings = c.fetchall()
    db.close()
    return player_standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    #Udacity reviewer suggested that three fields be used and omit result field
    #c.execute("INSERT INTO Matches_Tbl (winner_id, loser_id, result) VALUES (%s,%s,1)", (winner, loser))
    #c.execute("INSERT INTO Matches_Tbl (winner_id, loser_id, result) VALUES (%s,%s,0)", (loser, winner))
    c.execute("INSERT INTO Matches_Tbl (winner_id, loser_id) VALUES (%s,%s)", (winner, loser))
    db.commit()
    db.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    A list of tuples, each of which contains (id1, name1, id2, name2)
    Returns:
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    c = db.cursor()
    c .execute("SELECT id, name, number_wins FROM Standings_Vw ORDER BY number_wins DESC;")
    pairings_query = c.fetchall()
    db.close()

    i = 0
    pairs = []
    while i < len(pairings_query):
        player_1_id = pairings_query[i][0]
        player_1_name = pairings_query[i][1]
        player_2_id = pairings_query[i+1][0]
        player_2_name = pairings_query[i+1][0]
        pairs.append((player_1_id, player_1_name, player_2_id, player_2_name))
        i= i+2

    return pairs
