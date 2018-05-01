-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.



--drops the tables/views in the opposite order it was created
--this is because of dependencies

--these three lines were suggestes by a udacity reviewer
--these lines drop the database if it already exists and then creates it again
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;


DROP VIEW IF EXISTS Standings_Vw;
DROP VIEW IF EXISTS Game_Count_Vw;
DROP VIEW IF EXISTS Wins_Count_Vw;
DROP TABLE IF EXISTS Matches_Tbl;
DROP TABLE IF EXISTS Players_Tbl;


--players in the tournament
CREATE TABLE Players_Tbl
(
  id SERIAL PRIMARY KEY,
  name varchar(255)
);

--list the matches
--contains the id of the match
--player's id of the given match
--opponent's id of the given match
--the result 0 for a lose and 1 for wins
CREATE TABLE Matches_Tbl
(
  id Serial PRIMARY KEY,
  winner_id INTEGER REFERENCES Players_Tbl(id),
  loser_id INTEGER REFERENCES Players_Tbl(id)
);

--this is an old view statement
--CREATE VIEW Wins_Count_Vw AS
  --SELECT Players_Tbl.id, count(Matches_Tbl.loser_id) as number_wins
  --FROM Players_Tbl
  --LEFT JOIN (SELECT * FROM Matches_Tbl WHERE Matches_Tbl.result > 0) AS Matches_Tbl
  --ON Players_Tbl.id  = Matches_Tbl.winner_id
  --GROUP BY Players_Tbl.id;"""


  --displays the wins for all players
  --the numbers of wins is aggregated and counted
  --left join with players and matches
  CREATE VIEW Wins_Count_Vw AS
    SELECT Players_Tbl.id, count(Matches_Tbl.loser_id) as number_wins
    FROM Players_Tbl
    LEFT JOIN Matches_Tbl
    ON Players_Tbl.id  = Matches_Tbl.winner_id
    GROUP BY Players_Tbl.id;


--returns the number of games played by each players
--a unuion is used to combine the games a player won in and lost in
--from there count of all the games is summed up by each player
CREATE VIEW Game_Count_Vw AS
  SELECT total_games.id, sum(total_games.countOfGames) as number_Game
  From
  (
    SELECT Players_Tbl.id,  Count(Matches_Tbl.loser_id) AS countOfGames
    FROM Players_Tbl LEFT JOIN Matches_Tbl
    ON Players_Tbl.id = Matches_Tbl.loser_id
    GROUP BY Players_Tbl.id
    UNION ALL
    SELECT Players_Tbl.id, Count(Matches_Tbl.winner_id) AS countofGames
    FROM Players_Tbl LEFT JOIN Matches_Tbl
    ON Players_Tbl.id = Matches_Tbl.winner_id
    GROUP BY Players_Tbl.id
  ) as total_games
  Group By id;

--displays the standings for all players
--inudes player detail, name, wins, and total games
CREATE VIEW Standings_Vw AS
  SELECT Players_Tbl.id, Players_Tbl.name, Wins_Count_Vw.number_wins, Game_Count_Vw.number_game
  FROM Players_Tbl, Wins_Count_Vw, Game_Count_Vw
  WHERE Players_Tbl.id = Wins_Count_Vw.id AND Wins_Count_Vw.id = Game_Count_Vw.id;
