from RankingAlgorithms import PageRank
import sqlite3

TRANING_SET_SIZE = 0.3
dataset = sqlite3.connect('database.sqlite')

matches_query = dataset.execute('SELECT * FROM Match WHERE country_id=1729 ORDER BY date ASC')
pr = PageRank()

matches_fetch = matches_query.fetchall()
matches_count = len(matches_fetch)
training_set_border = math.ceil(matches_count*TRANING_SET_SIZE)

training_set = []
for i in range(training_set_border):
	row = matches_fetch[i]

	home_team_id = row[7]
	away_team_id = row[8]
	home_team_score = row[10]
	away_team_score = row[11]

	if home_team_id is not None and away_team_id is not None and home_team_score is not None and away_team_score is not None:
		pr.add_match(home_team_id, away_team_id, home_team_score, away_team_score)
		training_set.append(home_team_id, away_team_id, home_team_score, away_team_score)

pr.train(training_set)