from scipy.stats import norm

class Elo(object):
    def __init__(self, k_factor = 32, distribution = "logistics", sigma = 2000/7, x = 10, y = 400):
        self.k_factor = k_factor
        self.distribution = distribution
        self.sigma = sigma
        self.x = x
        self.y = y

    # r1: number representing first player's rating
    # r2: number representing seconds player's rating
    # 
    # returns a tuple of two numbers representing each player's expectancy to win
    def predict_winner(self, r1, r2):
        if self.distribution == "normal":
            d1 = norm(r1, self.sigma)
            d2 = norm(r2, self.sigma)
            intersect = (d1.mean() + d2.mean())/2
            e1 = d1.sf(intersect)
            e2 = 1-e1
        else:
            e1 = 1/(1+(self.x**((r2-r1)/self.y)))
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
    def rate_match(self, r1, r2, s1, s2 = None):
        if s2 is None:
            s2 = 1 - s1

        e1, e2 = self.predict_winner(r1, r2)

        r1_new = r1 + self.k_factor*(s1 - e1)
        r2_new = r2 + self.k_factor*(s2 - e2)

        return (r1_new, r2_new)

    # K_FACTOR: value the K_FACTOR should be set to
    # default value of K_FACTOR is 32
    def set_k_factor(self, k_factor):
        self.k_factor = k_factor

    # returns the K_FACTOR's current value
    def get_k_factor(self):
        return self.k_factor

    def set_distribution(self, distribution):
        self.distribution = distribution

    def get_distribution(self):
        return self.distribution

    def set_sigma(self, sigma):
        self.sigma = sigma

    def get_sigma(self):
        return self.sigma

    def set_x(self, x):
        self.x = x

    def get_x(self):
        return self.x

    def set_y(self, y):
        self.y = y

    def get_y(self):
        return self.get_y
