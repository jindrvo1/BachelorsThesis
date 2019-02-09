import sqlite3
from RankingAlgorithms import EloForTeams
import numpy as np

ELO_DEFAULT_RATING = 1200
elo_logistic = EloForTeams()
elo_normal = EloForTeams(distribution="normal")
dataset = sqlite3.connect('database.sqlite')
query = 'SELECT * FROM Match ORDER BY date ASC'
players_logistic_SA = {}
players_normal_SA = {}
players_logistic_CEM = {}
players_normal_CEM = {}
training_set_logistic_SA = []
training_set_normal_SA = []
training_set_logistic_CEM = []
training_set_normal_CEM = []

matches_fetch = dataset.execute(query)

for row in matches_fetch.fetchall():
    team1_logistic_SA, team2_logistic_SA = {}, {}
    team1_normal_SA, team2_normal_SA = {}, {}
    team1_logistic_CEM, team2_logistic_CEM = {}, {}
    team1_normal_CEM, team2_normal_CEM = {}, {}
    
    for index in range(55, 66):
        id = row[index]
        if id in players_logistic_SA:
            team1_logistic_SA[id] = players_logistic_SA[id]
        else:
            if id is not None:
                team1_logistic_SA[id] = ELO_DEFAULT_RATING
                
        if id in players_normal_SA:
            team1_normal_SA[id] = players_normal_SA[id]
        else:
            if id is not None:
                team1_normal_SA[id] = ELO_DEFAULT_RATING
                
        if id in players_logistic_CEM:
            team1_logistic_CEM[id] = players_logistic_CEM[id]
        else:
            if id is not None:
                team1_logistic_CEM[id] = ELO_DEFAULT_RATING
        
        if id in players_normal_CEM:
            team1_normal_CEM[id] = players_normal_CEM[id]
        else:
            if id is not None:
                team1_normal_CEM[id] = ELO_DEFAULT_RATING
        
    for index in range(66, 77):
        id = row[index]
        if id in players_logistic_SA:
            team2_logistic_SA[id] = players_logistic_SA[id]
        else:
            if id is not None:
                team2_logistic_SA[id] = ELO_DEFAULT_RATING
                
        if id in players_normal_SA:
            team2_normal_SA[id] = players_normal_SA[id]
        else:
            if id is not None:
                team2_normal_SA[id] = ELO_DEFAULT_RATING
                
        if id in players_logistic_CEM:
            team2_logistic_CEM[id] = players_logistic_CEM[id]
        else:
            if id is not None:
                team2_logistic_CEM[id] = ELO_DEFAULT_RATING
        
        if id in players_normal_CEM:
            team2_normal_CEM[id] = players_normal_CEM[id]
        else:
            if id is not None:
                team2_normal_CEM[id] = ELO_DEFAULT_RATING
                
    if len(team1_logistic_SA) == 11 and len(team2_logistic_SA) == 11:
        if row[9] > row[10]:
            score = 1
        elif row[9] < row[10]:
            score = 0
        else:
            score = 0.5
    
        training_set_logistic_SA.append([list(team1_logistic_SA.values()), list(team2_logistic_SA.values()), score])
        training_set_normal_SA.append([list(team1_normal_SA.values()), list(team2_normal_SA.values()), score])
        training_set_logistic_CEM.append([list(team1_logistic_CEM.values()), list(team2_logistic_CEM.values()), score])
        training_set_normal_CEM.append([list(team1_normal_CEM.values()), list(team2_normal_CEM.values()), score])
        
        team1_new, team2_new = elo_logistic.rate_match(list(team1_logistic_SA.values()), list(team2_logistic_SA.values()), score, 1-score)
        for id, rating in team1_logistic_SA.items():
            players_logistic_SA[id] = team1_new.pop(0)

        for id, rating in team2_logistic_SA.items():
            players_logistic_SA[id] = team2_new.pop(0)
            
        team1_new, team2_new = elo_normal.rate_match(list(team1_normal_SA.values()), list(team2_normal_SA.values()), score, 1-score)
        for id, rating in team1_normal_SA.items():
            players_normal_SA[id] = team1_new.pop(0)

        for id, rating in team2_normal_SA.items():
            players_normal_SA[id] = team2_new.pop(0)
            
        team1_new, team2_new = elo_logistic.rate_match(list(team1_logistic_CEM.values()), list(team2_logistic_CEM.values()), score, 1-score)
        for id, rating in team1_logistic_CEM.items():
            players_logistic_CEM[id] = team1_new.pop(0)

        for id, rating in team2_logistic_CEM.items():
            players_logistic_CEM[id] = team2_new.pop(0)
            
        team1_new, team2_new = elo_normal.rate_match(list(team1_normal_CEM.values()), list(team2_normal_CEM.values()), score, 1-score)
        for id, rating in team1_normal_CEM.items():
            players_normal_CEM[id] = team1_new.pop(0)

        for id, rating in team2_normal_CEM.items():
            players_normal_CEM[id] = team2_new.pop(0)

x_logistic_CEM, y_logistic_CEM = elo_logistic.CEM_train(training_set_logistic_CEM)
x_normal_CEM = elo_normal.CEM_train(training_set_normal_CEM)
x_logistic_SA, y_logistic_SA = elo_logistic.SA_train(training_set_logistic_SA)
x_normal_SA = elo_normal.SA_train(training_set_normal_SA)