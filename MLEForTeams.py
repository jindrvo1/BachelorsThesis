from scipy.optimize import minimize
from math import log
import sqlite3
from copy import copy
import numpy as np

def log_likelihood(scores):
	ll = 0
	global matches

	for match in matches:
		numerator = sum([scores[x] if match[0][x] == 1 else 0 for x in range(len(scores))])
		denumerator = sum([scores[x] if (match[0][x] == 1 or match[1][x] == 1) else 0 for x in range(len(scores))])
		ll += match[2]*log(numerator/denumerator) + (1-match[2])*log(1-numerator/denumerator)

	ll /= -len(matches)
	print('-------------------')
	print(np.mean(scores))
	print(np.std(scores))
	print(ll)
	return ll

dataset = sqlite3.connect('database.sqlite')
query = "SELECT * FROM Match WHERE country_id=1729 ORDER BY date ASC"
matches_query = dataset.execute(query)

"""
matches = [
	([1, 1, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0], 1),
	([1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1], 1),
	([0, 0, 0, 0, 1, 1], [0, 0, 1, 1, 0, 0], 0)
]

result = minimize(log_likelihood, [1 for x in range(6)], bounds=[(1, 100) for x in range(6)])

print("The ratings are {} with log log likelihood of {}.".format(result.x, result.fun))
"""

players = {}
matches = []
i = 0
for row in matches_query.fetchall():
	for index in range(55, 66):
		id = row[index]
		if id not in players and id is not None:
			players[id] = i
			i += 1

	for index in range(66, 77):
		id = row[index]
		if id not in players and id is not None:
			players[id] = i
			i += 1

matches_query = dataset.execute(query)
for row in matches_query.fetchall():
	players_t1 = copy(players)
	players_t2 = copy(players)

	for i, val in players_t1.items():
		players_t1[i] = 0

	for i, val in players_t2.items():
		players_t2[i] = 0

	for index in range(55, 66):
		id = row[index]
		players_t1[id] = 1

	for index in range(66, 77):
		id = row[index]
		players_t2[id] = 1

	team1 = list(players_t1.values())
	team2 = list(players_t2.values())

	if row[9] > row[10]:
		score = 1
	elif row[9] < row[10]:
		score = 0
	else:
		score = 0.5

	matches.append((team1, team2, score))

init = [1 for x in range(len(matches[0][0]))]

result = minimize(log_likelihood, [0.5 for x in range(len(init))], constraints=({'type':'eq', 'fun':lambda x:sum(x)-1}), bounds=[(0.01, 1) for x in range(len(init))])

print(result.x)
print(result.fun)
