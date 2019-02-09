import sqlite3
import math
from RankingAlgorithms import EloForTeams


TRANING_SET_SIZE = 0.5
ELO_DEFAULT_RATING = 1200
ELO_DEFAULT_MIN = 1000
ELO_DEFAULT_MAX = 1400
dataset = sqlite3.connect('database.sqlite')

# assign players a default rating based on the overall_rating column
players_fetch = dataset.execute('SELECT player_api_id, overall_rating from Player_Attributes')

players = {}
overall_rating = {}

for row in players_fetch:
	if row[0] is not None and row[1] is not None:
		overall_rating[row[0]] = row[1]

r_max = max(overall_rating.values())
r_min = min(overall_rating.values())
for p,r in overall_rating.items():
	players[p] = ((r-r_min)/(r_max-r_min))*(ELO_DEFAULT_MAX-ELO_DEFAULT_MIN)+ELO_DEFAULT_MIN


matches_query = dataset.execute('SELECT * FROM Match WHERE country_id=1729 ORDER BY date ASC')
elo = EloForTeams()

matches_fetch = matches_query.fetchall()

matches_count = len(matches_fetch)
training_set_border = math.ceil(matches_count*TRANING_SET_SIZE)

training_set = []

matches_total = 0
draws = 0
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
		matches_total += 1

		if row[9] > row[10]:
			score = 1
		elif row[9] < row[10]:
			score = 0
		else:	
			score = 0.5
			draws += 1

		training_set.append([list(team1.values()), list(team2.values()), score]);

		team1_new, team2_new = elo.rate_match(list(team1.values()), list(team2.values()), score, 1-score)

		for id, rating in team1.items():
			players[id] = team1_new.pop(0)

		for id, rating in team2.items():
			players[id] = team2_new.pop(0)

x, y = elo.train(training_set)

draws_percentage = draws/matches_total
success1 = 0
success2 = 0
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

		p1, p2 = elo.predict_winner_training(list(team1.values()), list(team2.values()), x, y)

		if p1 > 0.6 and score == 1 or p1 < 0.4 and score == 0 or p1 >= 0.4 and p1 <= 0.6 and score == 0.5:
			success1 += 1	

		if p1 < (0.5 - draws_percentage/2) and score == 0 or p1 >= (0.5 - draws_percentage/2) and p1 <= (0.5 + draws_percentage/2) and score == 0.5 or p1 > (0.5 + draws_percentage/2) and score == 1:
			success2 += 1

print("{},{}/{} were classified correctly.".format(success1, success2, matches_count - training_set_border))
