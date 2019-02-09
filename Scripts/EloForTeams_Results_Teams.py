import sqlite3
from RankingAlgorithms import Elo
import numpy as np

ELO_DEFAULT_RATING = 1200
dataset = sqlite3.connect('database.sqlite')
elo = Elo()
elo_normal = Elo(distribution="normal")
teams = {}
teams_normal = {}

for i in range(0, 2):
	total = 0
	total_normal = 0
	success = 0
	success_normal = 0
	ll = 0
	ll_normal = 0
	matches_fetch = dataset.execute('SELECT * FROM Match ORDER BY date ASC')
	for row in matches_fetch.fetchall():
		score1 = row[9]
		score2 = row[10]

		t1_id = row[7]
		if t1_id is not None:
			if t1_id in teams:
				team1 = teams[t1_id]
			else:
				team1 = ELO_DEFAULT_RATING

			if t1_id in teams_normal:
				team1_normal = teams_normal[t1_id]
			else:
				team1_normal = ELO_DEFAULT_RATING

		t2_id = row[8]
		if t2_id is not None:
			if t2_id in teams:
				team2 = teams[t2_id]
			else:
				team2 = ELO_DEFAULT_RATING

			if t2_id in teams_normal:
				team2_normal = teams_normal[t2_id]
			else:
				team2_normal = ELO_DEFAULT_RATING

		if score1 > score2:
			s = 1
		elif score1 < score2:
			s = 0
		else:
			s = 0.5

		if team1 is not None and team2 is not None:
			e1, e2 = elo.predict_winner(team1, team2)

			total += 1
			if e1 > 0.6 and s == 1 or e1 < 0.4 and s == 0 or e1 >= 0.4 and e1 <= 0.6 and s == 0.5:
				success += 1

			team1_new, team2_new = elo.rate_match(team1, team2, s, 1-s)

			teams[t1_id] = team1_new
			teams[t2_id] = team2_new

			w = 1 if s == 1 else 0
			ll += w*np.log(e1) + (1-w)*np.log(1-e1)

		if team1_normal is not None and team2_normal is not None:
			e1, e2 = elo_normal.predict_winner(team1_normal, team2_normal)

			total_normal += 1
			if e1 > 0.6 and s == 1 or e1 < 0.4 and s == 0 or e1 >= 0.4 and e1 <= 0.6 and s == 0.5:
				success_normal += 1

			team1_new, team2_new = elo_normal.rate_match(team1_normal, team2_normal, s, 1-s)

			teams_normal[t1_id] = team1_new
			teams_normal[t2_id] = team2_new

			w = 1 if s == 1 else 0
			ll_normal += w*np.log(e1) + (1-w)*np.log(1-e1)

	ll /= -total
	ll_normal /= -total_normal

print("Logistic distribution: ", success/total, ll)
print("Normal distribution: ", success_normal/total_normal, ll_normal)