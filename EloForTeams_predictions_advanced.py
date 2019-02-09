import sqlite3
from RankingAlgorithms import EloForTeams
from collections import OrderedDict
import math

ELO_DEFAULT_RATING = 1200
ELO_DEFAULT_MIN = 1000
ELO_DEFAULT_MAX = 1400
dataset = sqlite3.connect('database.sqlite')

# assign players a default rating based on the overall_rating column
players_fetch = dataset.execute('SELECT player_api_id, overall_rating from Player_Attributes')

players = {}
overall_rating = {}
"""
for row in players_fetch:
	if row[0] is not None and row[1] is not None:
		overall_rating[row[0]] = row[1]

r_max = max(overall_rating.values())
r_min = min(overall_rating.values())
for p,r in overall_rating.items():
	players[p] = ((r-r_min)/(r_max-r_min))*(ELO_DEFAULT_MAX-ELO_DEFAULT_MIN)+ELO_DEFAULT_MIN
"""

matches_fetch = dataset.execute('SELECT * FROM Match ORDER BY date ASC')

elo = EloForTeams()

# calculate the percentage of draws in all matches
draws = 0
matches = 0

for row in matches_fetch.fetchall():
	err = False

	for index in range(55, 77):
		if row[index] is None:
			err = True

	if err is False:
		matches += 1
		if row[9] == row[10]:
			draws += 1

draws_percentage = draws/matches

matches_fetch = dataset.execute('SELECT * FROM Match ORDER BY date ASC')

total = 0
well_predicted = 0
log_likelihood = 0
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

		# returns predictions
		e_t1, e_t2 = elo.predict_winner(list(team1.values()), list(team2.values()))

		total += 1
		if e_t1 > 0.6 and score == 1 or e_t1 < 0.4 and score == 0 or e_t1 >= 0.4 and e_t1 <= 0.6 and score == 0.5:
			well_predicted += 1

		w = 1 if score == 1 else 0
		log_likelihood += w*math.log(e_t1) + (1-w)*math.log(1-e_t1)

		# rate_match() returns tuple of two lists each consisting of eleven ratings
		team1_new, team2_new = elo.rate_match(list(team1.values()), list(team2.values()), score, 1-score)

		for id, rating in team1.items():
			players[id] = team1_new.pop(0)

		for id, rating in team2.items():
			players[id] = team2_new.pop(0)

log_likelihood /= -total

print("Predicting matches while rating players:")
print("Total numbers of matches: {}".format(total))
print("Correctly predicted: {}".format(well_predicted))
print("Ratio of correctly predicted: {}".format(well_predicted/total))
print("Log-likelihood: {}".format(log_likelihood))

matches_fetch = dataset.execute('SELECT * FROM Match ORDER BY date ASC')

total = 0
well_predicted = 0
log_likelihood = 0
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

		# returns predictions
		e_t1, e_t2 = elo.predict_winner(list(team1.values()), list(team2.values()))

		total += 1
		if e_t1 > 0.6 and score == 1 or e_t1 < 0.4 and score == 0 or e_t1 >= 0.4 and e_t1 <= 0.6 and score == 0.5:
			well_predicted += 1

		w = 1 if score == 1 else 0
		log_likelihood += w*math.log(e_t1) + (1-w)*math.log(1-e_t1)

log_likelihood /= -total

print("\nPredicting matches after players' ratings have been determined:")
print("Total numbers of matches: {}".format(total))
print("Correctly predicted: {}".format(well_predicted))
print("Ratio of correctly predicted: {}".format(well_predicted/total))
print("Log-likelihood: {}".format(log_likelihood))
