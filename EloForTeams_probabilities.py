import sqlite3
import math
from RankingAlgorithms import EloForTeams

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


matches_query = dataset.execute(query)
elo = EloForTeams()

players = {}

home_team = 0
away_team = 0
draw = 0
total = 0
success = 0
success_o = 0
success_ha = 0
success_ha_o = 0
log_likelihood = 0
log_likelihood_o = 0
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
			home_team += 1
		elif row[9] < row[10]:
			score = 0
			away_team += 1
		else:	
			score = 0.5
			draw += 1

		total += 1

		p1, p2 = elo.predict_winner(list(team1.values()), list(team2.values()))
		p1_o, p2_o = elo.predict_winner(list(team1_o.values()), list(team2_o.values()))

		home_modifier = 614/500

		if p1 > 0.5 and score == 1 or p1 <= 0.5 and score == 0:
			success += 1

		if p1_o > 0.5 and score == 1 or p1_o <= 0.5 and score == 0:
			success_o += 1

		p1 = p1*home_modifier if p1*home_modifier < 1 else 0.999
		p1_o = p1_o*home_modifier if p1*home_modifier < 1 else 0.999

		if p1 > 0.5 and score == 1 or p1 <= 0.5 and score == 0:
			success_ha += 1

		if p1_o > 0.5 and score == 1 or p1_o <= 0.5 and score == 0:
			success_ha_o += 1

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
		
		w = 1 if score == 1 else 0
		log_likelihood += w*math.log(p1) + (1-w)*math.log(1-p1)
		log_likelihood_o += w*math.log(p1_o) + (1-w)*math.log(1-p1_o)

log_likelihood /= -total
log_likelihood_o /= -total

matches_query = dataset.execute(query)

success_ha_o_a = 0
total_a = 0
for row in matches_query.fetchall():
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

	if len(team1) == 11 and len(team2) == 11:
		if row[9] > row[10]:
			score = 1
		elif row[9] < row[10]:
			score = 0
		else:	
			score = 0.5

		total_a += 1

		p1, p2 = elo.predict_winner(list(team1.values()), list(team2.values()))

		home_modifier = 614/500
		p1 = p1*home_modifier if p1*home_modifier < 1 else 0.999
		
		if p1 > 0.5 and score == 1 or p1 <= 0.5 and score == 0:
			success_ha_o_a += 1

print("{} out of {} were won by the home team ({}).".format(home_team, total, home_team/total))
print("{} out of {} were won by the away team ({}).".format(away_team, total, away_team/total))
print("{} out of {} were draws ({}).".format(draw, total, draw/total))
print("{} out of {} were predicted correctly ({}).".format(success, total, success/total))
print("{} out of {} were predicted correctly ({}).".format(success_o, total, success_o/total))
print("{} out of {} were predicted correctly ({}).".format(success_ha, total, success_ha/total))
print("{} out of {} were predicted correctly ({}).".format(success_ha_o, total, success_ha_o/total))
print("Log-likelihood: {}.".format(log_likelihood))
print("Log-likelihood: {}.".format(log_likelihood_o))
print("{} out of {} were predicted correctly ({}).".format(success_ha_o_a, total_a, success_ha_o_a/total_a))
