import sqlite3
import math
from RankingAlgorithms import EloForTeams2

ELO_DEFAULT_RATING = 1200
ELO_DEFAULT_MIN = 1000
ELO_DEFAULT_MAX = 1400
dataset = sqlite3.connect('database.sqlite')
query = "SELECT * FROM Match ORDER BY date ASC"

# assign players a default rating based on the overall_rating column
players_fetch = dataset.execute('SELECT player_api_id, overall_rating from Player_Attributes')

players_o = {}
overall_rating = {}

for row in players_fetch:
	if row[0] is not None and row[1] is not None:
		overall_rating[row[0]] = row[1]

r_max = max(overall_rating.values())
r_min = min(overall_rating.values())
for p,r in overall_rating.items():
	players_o[p] = ((r-r_min)/(r_max-r_min))*(ELO_DEFAULT_MAX-ELO_DEFAULT_MIN)+ELO_DEFAULT_MIN


# calculate the percentage of draws in all matches
matches_fetch = dataset.execute(query)

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

draws_perc = draws/matches

matches_query = dataset.execute(query)
elo = EloForTeams2()

players = {}

training_set = []
training_set_o = []

for row in matches_query.fetchall():
	team1, team2 = {}, {}
	team1_o, team2_o = {}, {}

	for index in range(55, 66):
		id = row[index]
		if id in players:
			team1[id] = players[id]
		else:
			if id is not None:
				team1[id] = ELO_DEFAULT_RATING

		if id in players_o:
			team1_o[id] = players_o[id]
		else:
			if id is not None:
				team1_o[id] = ELO_DEFAULT_RATING

	for index in range(66, 77):
		id = row[index]
		if id in players:
			team2[id] = players[id]
		else:
			if id is not None:
				team2[id] = ELO_DEFAULT_RATING

		if id in players_o:
			team2_o[id] = players_o[id]
		else:
			if id is not None:
				team2_o[id] = ELO_DEFAULT_RATING

	if len(team1) == 11 and len(team2) == 11:
		if row[9] > row[10]:
			score = 1
		elif row[9] < row[10]:
			score = 0
		else:	
			score = 0.5

		training_set.append([list(team1.values()), list(team2.values()), score]);
		training_set_o.append([list(team1_o.values()), list(team2_o.values()), score]);

		team1_new, team2_new = elo.rate_match(list(team1.values()), list(team2.values()), score, 1-score)
		team1_o_new, team2_o_new = elo.rate_match(list(team1_o.values()), list(team2_o.values()), score, 1-score)

		for id, rating in team1.items():
			players[id] = team1_new.pop(0)

		for id, rating in team2.items():
			players[id] = team2_new.pop(0)

		for id, rating in team1_o.items():
			players_o[id] = team1_o_new.pop(0)

		for id, rating in team2_o.items():
			players_o[id] = team2_o_new.pop(0)
	
x, y = elo.train(training_set)
x_o, y_o = elo.train(training_set_o)

matches_fetch = dataset.execute(query)

success = 0
success_o = 0
success_d = 0
success_d_o = 0
success_wl = 0
success_o_wl = 0
log_likelihood = 0
log_likelihood_o = 0
total = 0
success_o_ha_a = 0
for row in matches_fetch.fetchall():
	team1, team2 = {}, {}
	team1_o, team2_o = {}, {}

	for index in range(55, 66):
		id = row[index]
		if id in players:
			team1[id] = players[id]
		else:
			if id is not None:
				team1[id] = ELO_DEFAULT_RATING

		if id in players_o:
			team1_o[id] = players_o[id]
		else:
			if id is not None:
				team1_o[id] = ELO_DEFAULT_RATING

	for index in range(66, 77):
		id = row[index]
		if id in players:
			team2[id] = players[id]
		else:
			if id is not None:
				team2[id] = ELO_DEFAULT_RATING

		if id in players_o:
			team2_o[id] = players_o[id]
		else:
			if id is not None:
				team2_o[id] = ELO_DEFAULT_RATING

	if len(team1) == 11 and len(team2) == 11:
		if row[9] > row[10]:
			score = 1
		elif row[9] < row[10]:
			score = 0
		else:	
			score = 0.5

		p1, p2 = elo.predict_trained(list(team1.values()), list(team2.values()), x, y)
		p1_o, p2_o = elo.predict_trained(list(team1_o.values()), list(team2_o.values()), x_o, y_o)

		if p1 > 0.6 and score == 1 or p1 < 0.4 and score == 0 or p1 >= 0.4 and p1 <= 0.6 and score == 0.5:
			success += 1
		
		if p1_o > 0.6 and score == 1 or p1_o < 0.4 and score == 0 or p1_o >= 0.4 and p1_o <= 0.6 and score == 0.5:
			success_o += 1

		if p1 > (0.5 + draws_perc/2) and score == 1 or p1 < (0.5 - draws_perc/2) and score == 0 or p1 >= (0.5 - draws_perc/2) and p1 <= (0.5 + draws_perc/2) and score == 0.5:
			success_d += 1

		if p1_o > (0.5 + draws_perc/2) and score == 1 or p1_o < (0.5 - draws_perc/2) and score == 0 or p1_o >= (0.5 - draws_perc/2) and p1_o <= (0.5 + draws_perc/2) and score == 0.5:
			success_d_o += 1

		if p1 > 0.5 and score == 1 or p1 <= 0.5 and score == 0:
			success_wl += 1

		if p1_o > 0.5 and score == 1 or p1_o <= 0.5 and score == 0:
			success_o_wl += 1

		w = 1 if score == 1 else 0
		log_likelihood += w*math.log(p1) + (1-w)*math.log(1-p1)
		log_likelihood_o += w*math.log(p1_o) + (1-w)*math.log(1-p1_o)

		home_modifier = 614/500
		p1 = p1*home_modifier if p1*home_modifier < 1 else 0.999

		if p1 > 0.5 and score == 1 or p1 <= 0.5 and score == 0:
			success_o_ha_a += 1
			
		total += 1

log_likelihood /= total
log_likelihood_o /= total

print("{} out of {} were predicted correctly ({}).".format(success, total, success/total))
print("{} out of {} were predicted correctly ({}).".format(success_d, total, success_d/total))
print("{} out of {} were predicted correctly ({}).".format(success_o, total, success_o/total))
print("{} out of {} were predicted correctly ({}).".format(success_d_o, total, success_d_o/total))
print("{} out of {} were predicted correctly ({}).".format(success_wl, total, success_wl/total))
print("{} out of {} were predicted correctly ({}).".format(success_o_wl, total, success_o_wl/total))
print("Log-likelihood: {}.".format(log_likelihood))
print("Log-likelihood: {}.".format(log_likelihood_o))
print("{} out of {} were predicted correctly ({}).".format(success_o_ha_a, total, success_o_ha_a/total))
