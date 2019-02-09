import sqlite3
import trueskill as ts

dataset = sqlite3.connect('database.sqlite')

matches_fetch = dataset.execute('SELECT * FROM Match WHERE country_id=1729 ORDER BY date ASC')

players = {}

for row in matches_fetch.fetchall():
	team1, team2 = {}, {}

	for index in range(55, 66):
		id = row[index]
		if id in players:
			team1[id] = players[id]
		else:
			if id is not None:
				team1[id] = players[id] = ts.Rating()

	for index in range(66, 77):
		id = row[index]
		if id in players:
			team2[id] = players[id]
		else:
			if id is not None:
				team2[id] = players[id] = ts.Rating()

	ranks = [0, 0]
	if row[9] > row[10]:
		ranks = [0, 1]
	elif row[9] < row[10]:
		ranks = [1, 0]

	if len(team1) == 11 and len(team2) == 11:
		team1_new, team2_new = ts.rate([team1.values(), team2.values()], ranks=ranks)
		
		i = 0
		for p in team1:
			players[p] = team1_new[i]
			i += 1

		i = 0
		for p in team2:
			players[p] = team2_new[i]
			i += 1

print(players)