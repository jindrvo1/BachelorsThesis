import sqlite3
from RankingAlgorithms import EloForTeams
import pandas as pd
import matplotlib.pyplot as plt

elo = EloForTeams()
ELO_DEFAULT_RATING = 1200
dataset = sqlite3.connect('database.sqlite')
players = {}

df = pd.DataFrame(columns=['iteration', 'n_games'])

for i in range(1, 101):
    matches_fetch = dataset.execute('SELECT * FROM Match ORDER BY date ASC')

    total = 0
    well_predicted = 0
    for row in matches_fetch.fetchall():
        team1, team2 = {}, {}

        for index in range(55, 66):
            id = row[index]
            if id in players:
                team1[id] = players[id]
            else:
                if id is not None:
                    team1[id] = ELO_DEFAULT_RATING

        for index in range(66, 77):
            id = row[index]
            if id in players:
                team2[id] = players[id]
            else:
                if id is not None:
                    team2[id] = ELO_DEFAULT_RATING

        if len(team1) == 11 and len(team2) == 11:
            if row[9] > row[10]:
                score = 1
            elif row[9] < row[10]:
                score = 0
            else:
                score = 0.5

            e_t1, e_t2 = elo.predict_winner(list(team1.values()), list(team2.values()))

            total += 1
            if e_t1 > 0.6 and score == 1 or e_t1 < 0.4 and score == 0 or e_t1 >= 0.4 and e_t1 <= 0.6 and score == 0.5:
                well_predicted += 1

            team1_new, team2_new = elo.rate_match(list(team1.values()), list(team2.values()), score, 1-score)

            for id, rating in team1.items():
                players[id] = team1_new.pop(0)

            for id, rating in team2.items():
                players[id] = team2_new.pop(0)
                
    df = df.append({'iteration': i, 'n_games': well_predicted/total}, ignore_index=True)

plt.plot(df['iteration'], df['n_games'])

df.to_csv('../Files/MultipleTrainings.csv')