import sqlite3
import numpy as np

dataset = sqlite3.connect('database.sqlite')

matches_fetch = dataset.execute('SELECT * FROM Match ORDER BY date ASC')

data = {
	'home': {
		'Win': [0, 0],
		'Lose': [0, 0],
		'Draw': [0, 0],
	},
	'away': {
		'Win': [0, 0],
		'Lose': [0, 0],
		'Draw': [0, 0],
	}
}
for row in matches_fetch.fetchall():
	team1, team2 = [], []

	for index in range(55, 66):
		id = row[index]
		if id is not None:
			team1.append(id)

	for index in range(66, 77):
		id = row[index]
		if id is not None:
			team2.append(id)

	if len(team1) == 11 and len(team2) == 11:
		goals_home = row[9]
		goals_away = row[10]

		if goals_home is not None and goals_away is not None:
			if goals_home > goals_away:
				data['home']['Win'][0] += 1
				data['home']['Win'][1] += goals_home
				data['away']['Lose'][0] += 1
				data['away']['Lose'][1] += goals_away
			elif goals_home < goals_away:
				data['home']['Lose'][0] += 1
				data['home']['Lose'][1] += goals_home
				data['away']['Win'][0] += 1
				data['away']['Win'][1] += goals_away
			else:
				data['home']['Draw'][0] += 1
				data['home']['Draw'][1] += goals_home
				data['away']['Draw'][0] += 1
				data['away']['Draw'][1] += goals_away

print("home_away,outcome,goalspergame")
for home_away, outcome in data.items():
	for key, arr in outcome.items():
		print(home_away, end=',')
		print(key, end=',')
		print(arr[1]/arr[0])
