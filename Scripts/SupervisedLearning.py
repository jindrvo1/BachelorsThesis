import pandas as pd
import numpy as np
import sqlite3

dataset = sqlite3.connect('database.sqlite')

cols = ['home_team_goal', 'away_team_goal']
for prefix in ['home_player_', 'away_player_']:
    for i in range(1, 12):
        cols.append(prefix+str(i))

df = pd.DataFrame(columns=cols)
p = pd.DataFrame(columns=['player_api_id'])

matches_fetch = dataset.execute('SELECT * FROM Match ORDER BY date ASC')

for row in matches_fetch.fetchall():
    team1, team2 = [], []
    
    for index in range(55, 66):
        id = row[index]
        if id is not None:
            team1.append(id)

    for index in range(66, 77):
        id = row[index]
        if id is not None:
            team2.append(id)
    
    home_team_score = row[9]
    away_team_score = row[10]
    
    if len(team1) == 11 and len(team2) == 11 and home_team_score is not None and away_team_score is not None:
        row = {'home_team_goal': home_team_score, 'away_team_goal': away_team_score}
        
        i = 1
        for player in team1:
            if player not in p['player_api_id'].values:
                p = p.append({'player_api_id': player}, ignore_index=True)
                
            row['home_player_{}'.format(i)] = player
            i += 1
            
        i = 1
        for player in team2:
            if player not in p['player_api_id'].values:
                p = p.append({'player_api_id': player}, ignore_index=True)
                
            row['away_player_{}'.format(i)] = player
            i += 1
            
        df = df.append(row, ignore_index=True)

players = {}

for i, k in enumerate(p['player_api_id']):
    players[k] = i
    
ix_players = {v:k for k,v in players.items()}

n_players = len(players)
n_matches = df.shape[0]
team_length = 11

def vectorize_match(match_id):
    # Initialize vector
    vector = np.zeros(n_players)
    
    # Put the winners and losers
    for j in range(0,team_length):
        vector[players[df.iloc[match_id,j+2]]] = 1
        vector[players[df.iloc[match_id,j+2+team_length]]] = -1        
    return vector

vec = np.zeros(n_players)
X = np.array([vectorize_match(match_id) for match_id in range(df.shape[0])])

from keras.utils import to_categorical

y = np.round((((df['home_team_goal']-df['away_team_goal'])/abs(0.01+df['home_team_goal']-df['away_team_goal'])).values).astype(np.double))
y = to_categorical(y, num_classes=3)

# Split in validation and training data 
train_idx = int(0.8*X.shape[1])
X_train = X[0:train_idx,:]
X_test = X[train_idx:,:]
y_train = y[0:train_idx]
y_test = y[train_idx:]

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers.advanced_activations import LeakyReLU

model = Sequential()
model.add(Dense(10, input_dim=X_train.shape[1], activation='linear'))
model.add(Dropout(0.4))
model.add(Dense(3, activation='softmax'))

num_epochs = 20
batch_size = 2

model.compile(optimizer='rmsprop',loss='categorical_crossentropy')

history = model.fit(X_train, y_train, epochs=num_epochs, batch_size=batch_size, validation_data=(X_test,y_test))

raw_preds = model.predict(X_test)

outcomes_guessed = sum([np.argmax(y_test[j])==np.argmax(raw_preds[j]) for j in range(y_test.shape[0])])/y_test.shape[0]*100
print("Outcomes guessed: ", outcomes_guessed)