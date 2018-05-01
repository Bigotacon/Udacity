from tournament import *


#registers players
registerPlayer("April")
registerPlayer("Josh")



#displays the players
db = connect()
c = db.cursor()
display_standing_query = "SELECT * FROM Players_Tbl;"
c.execute(display_standing_query)
players = c.fetchall()
print "the players are"
print players
db.close()


#
reportMatch(1, 2)

db = connect()
c = db.cursor()
display_standing_query = "SELECT * FROM Matches_Tbl;"
c.execute(display_standing_query)
matches = c.fetchall()
print "the matches are "
print  matches
db.close()


db = connect()
c = db.cursor()
display_standing_query = "SELECT * FROM Standings_Vw;"
c.execute(display_standing_query)
standings = c.fetchall()
print "the standings are :"
print  standings
db.close()

swissPairings()

deleteMatches()
deletePlayers()
