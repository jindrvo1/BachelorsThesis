import sqlite3

dataset = sqlite3.connect('database.sqlite')
query = "SELECT * FROM Match WHERE country_id=1729 ORDER BY date ASC"
matches_query = dataset.execute(query)

players = {}
matches = []

for row in matches_query.fetchall():
	team1, team2 = [], []

	for index in range(55, 66):
		id = row[index]
		if id is not None:
			team1.append(id)

	for index in range(66, 77):
		id = row[index]
		if id is not None:
			team2.append(id)

	if row[9] > row[10]:
		score = 1
	elif row[9] < row[10]:
		score = 0
	else:
		score = 0.5

	if len(team1) == 11 and len(team2) == 11:
		matches.append((team1, team2, score))

success = 0
total = 0
for match in matches:
	t1_s = 0
	t1_players = 0
	for p1 in match[0]:
		p1_t_s = 0
		n_players = 0
		for p2 in match[1]:
			p1_w = 0
			p1_l = 0
			n_matches = 0
			for m in matches:
				if p1 in m[0] and p2 in m[1]:
					if m[2] == 1:
						p1_w += 1
						n_matches += 1
					elif m[2] == 0:
						p1_l += 1
						n_matches += 1
				elif p1 in m[1] and p2 in m[0]:
					if m[2] == 0:
						p1_l += 1
						n_matches += 1
					elif m[2] == 1:
						p1_w += 1
						n_matches += 1
			if n_matches > 0:
				p1_t_s += p1_w/(p1_w+p1_l)
				n_players += 1
			else:
				p1_t_s += 0.5
				n_players += 1
		p1_t_s /= n_players
		t1_s += p1_t_s
		t1_players += 1
	t1_s /= t1_players
	print(t1_s)
	if t1_s >= 0.5 and match[2] == 1:
		success += 1
	elif t1_s < 0.5 and match[2] == 0:
		success += 1
	
	if match[2] == 1 or match[2] == 0:
		total += 1

print("{} out of {} (={})".format(success, total, success/total))