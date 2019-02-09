class Elo(object):
    def __init__(self, K_FACTOR = 32):
        self.K_FACTOR = K_FACTOR

    # r1: number representing first player's rating
    # r2: number representing seconds player's rating
    # 
    # returns a tuple of two numbers representing each player's expectancy to win
    def predict_winner(self, r1, r2):
        e1 = 1/(1+(10**((r2-r1)/400)))
        e2 = 1-e1

        return (e1, e2)
    
    # r1: number representing first player's rating
    # r2: number representing seconds player's rating
    # s1: 0/0.5/1 number representing first player's score
    # s2: 0/0.5/1 number representing seconds player's score
    # scores have to add up to 1, leaving us with only three possible scenarios ([0,1],[1,0],[0.5,0.5])
    # score of 0 means the player lost, score of 1 means he won and score of 0.5 means the match was a draw
    #
    # returns a tuple of two numbers representing each player's new rating
    def rate_match(self, r1, r2, s1, s2):
        e1, e2 = self.predict_winner(r1, r2)

        r1_new = r1 + self.K_FACTOR*(s1 - e1)
        r2_new = r2 + self.K_FACTOR*(s2 - e2)

        return (r1_new, r2_new)

    # K_FACTOR: value the K_FACTOR should be set to
    # default value of K_FACTOR is 32
    def set_k_factor(self, K_FACTOR):
        self.K_FACTOR = set_k_factor

    # returns the K_FACTOR's current value
    def get_k_factor(self):
        return self.K_FACTOR