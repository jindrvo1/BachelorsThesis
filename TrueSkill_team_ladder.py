import sqlite3
import trueskill as ts
from collections import OrderedDict

dataset = sqlite3.connect('database.sqlite')

matches_fetch = dataset.execute('SELECT * FROM Match ORDER BY date ASC')

teams = {}

for row in matches_fetch.fetchall():
	home_team_id = row[7]
	away_team_id = row[8]

	if home_team_id is not None and away_team_id is not None:
		if home_team_id not in teams:
			teams[home_team_id] = ts.Rating()

		if away_team_id not in teams:
			teams[away_team_id] = ts.Rating()

		teams[home_team_id], teams[away_team_id] = ts.rate_1vs1(teams[home_team_id], teams[away_team_id])

teams_fetch = dataset.execute('SELECT * FROM Team')
team_names = {}

for row in teams_fetch.fetchall():
	team_api_id = row[1]
	team_name = row[4]

	if team_api_id is not None:
		team_names[team_api_id] = team_name

ladder_vals = {}
for team, rating in teams.items():
	ladder_vals[team] = rating.mu - 3*rating.sigma

minimum = min(ladder_vals.values())
maximum = max(ladder_vals.values())

ladder_vals_norm = {}
for team, cons_estimate in ladder_vals.items():
	ladder_vals_norm[team_names[team]] = (cons_estimate-minimum)/(maximum-minimum)

ladder = OrderedDict(sorted(ladder_vals_norm.items(), key=lambda x:x[1]))

print("Team,Rating")
for team, rating in ladder.items():
	print("{},{}".format(team, rating))