import sqlite3
from RankingAlgorithms import PageRank
from math import log

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

for i in range(0, 10):
	pageranks = pr.calculate_pagerank(i)
	"""
	pagerank_norm = {}

	# normalize pageranks onto <0;1> interval
	minimum = min(pageranks.values())
	maximum = max(pageranks.values())

	for team_id, pagerank in pageranks.items():
		if team_id not in pagerank_norm:
			pagerank_norm[team_id] = {}

		pagerank_norm[team_id] = (pagerank-minimum)/(maximum-minimum)
	"""
	matches_fetch = dataset.execute('SELECT * FROM Match ORDER BY date ASC')

	total = 0
	success = 0
	log_likelihood = 0
	for row in matches_fetch.fetchall():
		home_team_id = row[7]
		away_team_id = row[8]
		home_team_score = row[10]
		away_team_score = row[11]
		date = row[5][:10]

		if home_team_id is not None and away_team_id is not None and home_team_score is not None and away_team_score is not None:
			#home_team_pr = pagerank_norm[home_team_id]
			#away_team_pr = pagerank_norm[away_team_id]
			home_team_pr = pageranks[home_team_id]
			away_team_pr = pageranks[away_team_id]

			p = home_team_pr/(home_team_pr+away_team_pr)

			score = 0.5

			if home_team_score > away_team_score:
				score = 1
			elif home_team_score < away_team_score:
				score = 0

			if p > 0.6 and score == 1 or p < 0.4 and score == 0 or p >= 0.4 and p <= 0.6 and score == 0.5:
				success += 1

			w = 1 if score == 1 else 0
			log_likelihood += w*log(p) + (1-w)*log(1-p)

			total += 1

	log_likelihood /= -total

	print("Function #{}".format(i))
	print("{} out of {} were predicted correctly ({}).".format(success, total, success/total))
	print("Log-likelihood: {}".format(log_likelihood))