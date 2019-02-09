import sqlite3
import math
from RankingAlgorithms import EloForTeams


TRANING_SET_SIZE = 0.5
ELO_DEFAULT_RATING = 1200
dataset = sqlite3.connect('database.sqlite')

matches_query = dataset.execute('SELECT * FROM Match WHERE country_id=1729 ORDER BY date ASC')
elo = EloForTeams()

players = {}

matches_fetch = matches_query.fetchall()

matches_count = len(matches_fetch)
training_set_border = math.ceil(matches_count*TRANING_SET_SIZE)

training_set = []

for i in range(training_set_border):
	team1, team2 = {}, {}
	row = matches_fetch[i]

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

	if len(team1) == 11 and len(team2) == 11:
		if row[9] > row[10]:
			score = 1
		elif row[9] < row[10]:
			score = 0
		else:	
			score = 0.5

		training_set.append([list(team1.values()), list(team2.values()), score]);

		team1_new, team2_new = elo.rate_match(list(team1.values()), list(team2.values()), score, 1-score)

		for id, rating in team1.items():
			players[id] = team1_new.pop(0)

		for id, rating in team2.items():
			players[id] = team2_new.pop(0)
	
x, y = elo.train(training_set)

success = 0
for i in range(training_set_border, matches_count):
	team1, team2 = {}, {}
	row = matches_fetch[i]

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

	if len(team1) == 11 and len(team2) == 11:
		if row[9] > row[10]:
			score = 1
		elif row[9] < row[10]:
			score = 0
		else:	
			score = 0.5

		p = elo.predict_trained(list(team1.values()), list(team2.values()), x, y)

		if p > 0.6 and score == 1 or p < 0.4 and score == 0 or p >= 0.4 and p <= 0.6 and score == 0.5:
			success += 1	

print("{}/{} were classified correctly.".format(success, matches_count - training_set_border))