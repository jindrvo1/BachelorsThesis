import sqlite3
from RankingAlgorithms import PageRank
from collections import OrderedDict

dataset = sqlite3.connect('database.sqlite')

matches_fetch = dataset.execute('SELECT * FROM Match ORDER BY date ASC')
pr = PageRank()

for row in matches_fetch.fetchall():
	home_team_id = row[7]
	away_team_id = row[8]
	home_team_score = row[10]
	away_team_score = row[11]

	if home_team_id is not None and away_team_id is not None and home_team_score is not None and away_team_score is not None:
		pr.add_match(home_team_id, away_team_id, home_team_score, away_team_score)

teams_fetch = dataset.execute('SELECT * FROM Team')
teams = {}

for row in teams_fetch.fetchall():
	team_api_id = row[1]
	team_name = row[4]

	if team_api_id is not None:
		teams[team_api_id] = team_name

results = {}

pageranks = pr.calculate_pagerank(0)

minimum = min(pageranks.values())
maximum = max(pageranks.values())

for team_id, pagerank in pageranks.items():
	# pageranks are normalized onto <0;1> interval
	results[teams[team_id]] = (pagerank-minimum)/(maximum-minimum)

# sorts teams dictionary by rating, creating an ascendingly sorted ladder
ladder = OrderedDict(sorted(results.items(), key=lambda x:x[1]))		

print("Team,PR")
for team, pr in ladder.items():
	print("{},{}".format(team, pr))