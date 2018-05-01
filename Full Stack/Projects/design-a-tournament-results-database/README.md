rdb-fullstack
=============

Common code for the Relational Databases and Full Stack Fundamentals courses
Files
•	Tournament.py—this is the implementation of a Swiss-system tournament
•	Tournament.sql—Schema and methods for the tournament project
•	Tournament_test.py—Tests Tournament.py to see if it meets specification

Instructions
1.	Load the schema by entering the following in the terminal: /vagrant/tournament$ psql tournament < tournament.sql
2.	Test the Tournament by entering the following: /vagrant/tournament$ python tournament_test.py
3.	The terminal will print the results for up to six projects

Overview
This project supports a Swiss-Pairing Tournament. THis project stores players information, registers players, records the winners of a game, and reports the standing of the entire tournament. In addtion this project can count the number of players registered and drop players and/or matches.
