import sqlite3
import numpy as np

dataset = sqlite3.connect('database.sqlite')

matches_fetch = dataset.execute('SELECT * FROM Match ORDER BY date ASC')

data = {
	'total': 0,
	'useful': 0,
	'home_win': 0,
	'away_win': 0,
	'draw': 0,
	'goals_home': {},
	'goals_away': {}
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

	data['total'] += 1
	if len(team1) == 11 and len(team2) == 11:
		goals_home = row[9]
		goals_away = row[10]
		data['useful'] += 1

		if goals_home is not None and goals_away is not None:
			if goals_home > goals_away:
				data['home_win'] += 1
			elif goals_home < goals_away:
				data['away_win'] += 1
			else:
				data['draw'] += 1

		if goals_home is not None:
			if goals_home in data['goals_home']:
				data['goals_home'][goals_home] += 1
			else:
				data['goals_home'][goals_home] = 1

		if goals_away is not None:
			if goals_away in data['goals_away']:
				data['goals_away'][goals_away] += 1
			else:
				data['goals_away'][goals_away] = 1

#print(data)

s_h, s_a = 0, 0
m_h, m_a = 0, 0
for goals, games in data['goals_home'].items():
	s_h += goals*games
	m_h += games

for goals, games in data['goals_away'].items():
	s_a += goals*games
	m_a += games

#print("Home goal mean: ", s_h/m_h)
#print("Away goal mean: ", s_a/m_a)
ratings_fetch = dataset.execute('SELECT player_api_id, overall_rating FROM Player_Attributes ORDER BY date ASC')
ratings = {}
for row in ratings_fetch.fetchall():
	if row[0] is not None and row[1] is not None:
		ratings[row[0]] = row[1]

print("rating")
for rating in ratings.values():
	print(rating)