import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

dataset = sqlite3.connect('database.sqlite')
matches_fetch = dataset.execute('SELECT * FROM Match ORDER BY date ASC')

p = {}

for row in matches_fetch:
    team1, team2 = [], []

    for index in range(55, 66):
        id = row[index]
        if id is not None:
            team1.append(id)

    for index in range(66, 77):
        id = row[index]
        if id is not None:
            team2.append(id)

    if len(team1) == 11 and len(team2) == 11:
        for id in team1:
            if id not in p:
                p[id] = 1
            else:
                p[id] += 1

        for id in team2:
            if id not in p:
                p[id] = 1
            else:
                p[id] += 1
df = pd.DataFrame({
    'id': list(p.keys()),
    'n_games': list(p.values())
})

plt.hist(df['n_games'])
plt.axvline(x=df['n_games'].mean(), color="red")
plt.axvline(x=df['n_games'].median(), color="red")