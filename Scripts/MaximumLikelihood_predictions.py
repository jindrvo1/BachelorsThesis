import sqlite3

dataset = sqlite3.connect('database.sqlite')

matches_fetch = dataset.execute('SELECT * FROM Match ORDER BY date ASC')

success = 0
total = 0
totaltotal = 0
for row in matches_fetch.fetchall():
	score = 0.5
	totaltotal += 1
	
	if row[9] > row[10]:
		score = 1
	elif row[9] < row[10]:
		score = 0

	
	curr_date = row[5]
	home_team = row[7]
	away_team = row[8]

	relevant_matches_fetch = dataset.execute('SELECT * FROM Match WHERE date < \'{date}\' AND (home_team_api_id = {home_team} AND away_team_api_id = {away_team} OR home_team_api_id = {away_team} AND away_team_api_id = {home_team})'.format(date=curr_date, home_team=home_team, away_team=away_team))

	matches_won = 0
	matches_lost = 0
	for rel_row in relevant_matches_fetch.fetchall():
		home_team_score = rel_row[9]
		away_team_score = rel_row[10]

		if home_team_score > away_team_score:
			matches_won += 1
		elif home_team_score < away_team_score:
			matches_lost += 1

	if matches_won + matches_lost > 0:
		p = matches_won/(matches_won+matches_lost)
	else:
		p = 0.5

	if p < 0.4 and score == 0 or p > 0.6 and score == 1 or p >= 0.4 and p <= 0.6 and score == 0.5:
		success += 1

	total += 1

print("{} out of {} were predicted correctly ({}).".format(success, total, success/total))
