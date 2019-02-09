import sqlite3
from RankingAlgorithms import EloForTeams

elo = EloForTeams()

ELO_DEFAULT_RATING = 1200
ELO_DEFAULT_MIN = 1000
ELO_DEFAULT_MAX = 1400
dataset = sqlite3.connect('database.sqlite')
query = 'SELECT * FROM Match ORDER BY date ASC'

players = {}

matches_fetch = dataset.execute(query)

for row in matches_fetch.fetchall():
	team1, team2 = {}, {}

	for index in range(55, 66):
		id = row[index]
		if id in players:
			team1[id] = players[id]
		else:
			if id is not None:
				team1[id] = ELO_DEFAULT_RATING

	for index in range(66, 77):
		id = row[index]
		if id in players:
			team2[id] = players[id]
		else:
			if id is not None:
				team2[id] = ELO_DEFAULT_RATING

	# do not proceed unless there are exactly 11 player's in both teams
	if len(team1) == 11 and len(team2) == 11:
		if row[9] > row[10]:
			score = 1
		elif row[9] < row[10]:
			score = 0
		else:	
			score = 0.5

		team1_new, team2_new = elo.rate_match(list(team1.values()), list(team2.values()), score, 1-score)

		for id, rating in team1.items():
			players[id] = team1_new.pop(0)

		for id, rating in team2.items():
			players[id] = team2_new.pop(0)

matches_fetch = dataset.execute(query)

matches_diffs = {'won': [], 'lost': [], 'draw': []}
for row in matches_fetch.fetchall():
	team1, team2 = {}, {}

	for index in range(55, 66):
		id = row[index]
		if id in players:
			team1[id] = players[id]
		else:
			if id is not None:
				team1[id] = ELO_DEFAULT_RATING

	for index in range(66, 77):
		id = row[index]
		if id in players:
			team2[id] = players[id]
		else:
			if id is not None:
				team2[id] = ELO_DEFAULT_RATING

	# do not proceed unless there are exactly 11 player's in both teams
	if len(team1) == 11 and len(team2) == 11:
		matches_index = 'draw'
		if row[9] > row[10]:
			matches_index = 'won'
		elif row[9] < row[10]:
			matches_index = 'lost'

		r1, r2 = elo.teams_ratings(list(team1.values()), list(team2.values()))
		matches_diffs[matches_index].append(r1 - r2)


#print("Won: {}".format(sum(matches_diffs['won'])/len(matches_diffs['won'])))
#print("Lost: {}".format(sum(matches_diffs['lost'])/len(matches_diffs['lost'])))
#print("Draw: {}".format(sum(matches_diffs['draw'])/len(matches_diffs['draw'])))

for m in matches_diffs['lost']:
	print(m)
