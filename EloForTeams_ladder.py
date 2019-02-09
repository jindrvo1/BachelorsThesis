import sqlite3
from RankingAlgorithms import EloForTeams
from collections import OrderedDict

# Player class
# id is the database's player_api_id column
# name is the player's name obtained from Players table
# ratings is an ordered dictionary with dates of matches as keys and ratings as values - this allows us to track player's changes in elo over time
class Player(object):
	def __init__(self, id, name):
		self.id = id
		self.name = name
		self.ratings = OrderedDict()

	def get_ratings(self):
		return self.ratings

	def add_rating(self, date, rating):
		self.ratings[date] = rating

	def last_rating(self):
		return self.ratings[next(reversed(self.ratings))]

ELO_DEFAULT_RATING = 1200
dataset = sqlite3.connect('database.sqlite')

matches_fetch = dataset.execute('SELECT * FROM Match WHERE country_id=1729 ORDER BY date ASC')
elo = EloForTeams()

# dictionary of players with database's player_api_id as key and a Player object as value
players = {}

for row in matches_fetch.fetchall():
	team1, team2 = {}, {}

	for index in range(55, 66):
		id = row[index]
		if id in players:
			team1[id] = players[id].last_rating()
		else:
			if id is not None:
				team1[id] = ELO_DEFAULT_RATING

	for index in range(66, 77):
		id = row[index]
		if id in players:
			team2[id] = players[id].last_rating()
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

		# all the times in database are 00:00:00, thus we can ommit that part
		date = row[5][:10]

		# rate_match() returns tuple of two lists each consisting of eleven ratings
		team1_new, team2_new = elo.rate_match(list(team1.values()), list(team2.values()), score, 1-score)

		for id, rating in team1.items():
			if id in players:
				players[id].add_rating(date, team1_new.pop(0))
			else:
				player_fetch = dataset.execute('SELECT * FROM Player WHERE player_api_id={}'.format(id))
				player_row = player_fetch.fetchone()
				if player_row is not None:
					players[id] = Player(id, player_row[2])
					players[id].add_rating(date, team1_new.pop(0))

		for id, rating in team2.items():
			if id in players:
				players[id].add_rating(date, team2_new.pop(0))
			else:
				player_fetch = dataset.execute('SELECT * FROM Player WHERE player_api_id={}'.format(id))
				player_row = player_fetch.fetchone()
				if player_row is not None:
					players[id] = Player(id, player_row[2])
					players[id].add_rating(date, team2_new.pop(0))

# sorts players dictionary by rating, creating an ascendingly sorted ladder
ladder = OrderedDict(sorted(players.items(), key=lambda x:x[1].last_rating()))

# obtains the player in the ladder
best_player = ladder[next(reversed(ladder))]

print("Date,Rating")
for date, rating in best_player.get_ratings().items():
	print("{},{}".format(date, rating))