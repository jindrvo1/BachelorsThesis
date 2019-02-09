import sqlite3
from RankingAlgorithms import EloForTeams
import numpy as np

ELO_DEFAULT_RATING = 1200
elo_logistic = EloForTeams()
elo_normal = EloForTeams(distribution="normal")
dataset = sqlite3.connect('database.sqlite')
query = 'SELECT * FROM Match ORDER BY date ASC'
players_logistic = {}
players_normal = {}

for i in range(0, 2):
    matches_fetch = dataset.execute(query)

    total_logistic = 0
    total_normal = 0
    predicted_logistic = 0
    predicted_normal = 0
    log_likelihood_logistic = 0
    log_likelihood_normal = 0

    for row in matches_fetch.fetchall():
        team1_logistic, team2_logistic = {}, {}
        team1_normal, team2_normal = {}, {}

        for index in range(55, 66):
            id = row[index]
            if id in players_logistic:
                team1_logistic[id] = players_logistic[id]
            else:
                if id is not None:
                    team1_logistic[id] = ELO_DEFAULT_RATING
                    
            if id in players_normal:
                team1_normal[id] = players_normal[id]
            else:
                if id is not None:
                    team1_normal[id] = ELO_DEFAULT_RATING

        for index in range(66, 77):
            id = row[index]
            if id in players_logistic:
                team2_logistic[id] = players_logistic[id]
            else:
                if id is not None:
                    team2_logistic[id] = ELO_DEFAULT_RATING
                    
            if id in players_normal:
                team2_normal[id] = players_normal[id]
            else:
                if id is not None:
                    team2_normal[id] = ELO_DEFAULT_RATING

        if row[9] > row[10]:
            score = 1
        elif row[9] < row[10]:
            score = 0
        else:
            score = 0.5

        if len(team1_logistic) == 11 and len(team2_logistic) == 11:
            e1_l, e2_l = elo_logistic.predict_winner(list(team1_logistic.values()), list(team2_logistic.values()))
            
            e1_l = 1.228*e1_l if 1.228*e1_l < 1 else 0.999
            e2_l = 1 - e1_l
            
            total_logistic += 1
            
            if e1_l >= 0.5 and score == 1 or e1_l < 0.5 and score == 0:
                predicted_logistic += 1

            w = 1 if score == 1 else 0
            log_likelihood_logistic += w*np.log(e1_l) + (1-w)*np.log(1-e1_l)

            team1_new, team2_new = elo_logistic.rate_match(list(team1_logistic.values()), list(team2_logistic.values()), score, 1-score)

            for id, rating in team1_logistic.items():
                players_logistic[id] = team1_new.pop(0)

            for id, rating in team2_logistic.items():
                players_logistic[id] = team2_new.pop(0)

        if len(team1_normal) == 11 and len(team2_normal) == 11:
            e1_n, e2_n = elo_normal.predict_winner(list(team1_normal.values()), list(team2_normal.values()))

            e1_n = 1.228*e1_n if 1.228*e1_n < 1 else 0.999
            e1_n = 1 - e1_n

            total_normal += 1

            if e1_n >= 0.5 and score == 1 or e1_n < 0.5 and score == 0:
                predicted_normal += 1

            w = 1 if score == 1 else 0
            log_likelihood_normal += w*np.log(e1_n) + (1-w)*np.log(1-e1_n)

            team1_new, team2_new = elo_normal.rate_match(list(team1_normal.values()), list(team2_normal.values()), score, 1-score)

            for id, rating in team1_normal.items():
                players_normal[id] = team1_new.pop(0)

            for id, rating in team2_normal.items():
                players_normal[id] = team2_new.pop(0)

    log_likelihood_logistic /= -total_logistic
    log_likelihood_normal /= -total_normal

print("Logistic distribution: ", predicted_logistic/total_logistic, log_likelihood_logistic)
print("Normal distribution: ", predicted_normal/total_normal, log_likelihood_normal)