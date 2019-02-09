from math import exp, sqrt
from random import seed, random, normalvariate

class EloForTeams3(object):
    def __init__(self, K_FACTOR = 32):
        self.K_FACTOR = K_FACTOR

    # t1: list of first team's players' ratings
    # t2: list of seconds team's players' ratings
    #
    # returns a tuple of two numbers representing each team's expectancy to win
    def predict_winner(self, t1, t2):
        r_t1, r_t2 = self.teams_ratings(t1, t2)

        e_t1 = 1.0/(1+10**((r_t2-r_t1)/400))
        e_t2 = 1-e_t1

        return (e_t1, e_t2)

    # t1: list of first team's players' ratings
    # t2: list of seconds team's players' ratings
    # s_t1: 0/0.5/1 number representing first team's score
    # s_t2: 0/0.5/1 number representing seconds team's score
    # scores have to add up to 1, leaving us with only three possible scenarios ([0,1],[1,0],[0.5,0.5])
    # score of 0 means the team lost, score of 1 means it won and score of 0.5 means the match was a draw
    #
    # returns a tuple of two lists of numbers, each list representing of two teams, each number representing each player's new rating
    def rate_match(self, t1, t2, s_t1, s_t2):
        r_t1, r_t2 = self.teams_ratings(t1, t2)
        e_t1, e_t2 = self.predict_winner(t1, t2)

        r_t1_new = r_t1 + self.K_FACTOR*(s_t1-e_t1)
        r_t2_new = r_t2 + self.K_FACTOR*(s_t2-e_t2)

        t1_new = [r + (r_t1_new-r_t1)*(r_t1_new/r)**(2*s_t1-1) for r in t1]
        t2_new = [r + (r_t2_new-r_t2)*(r_t2_new/r)**(2*s_t2-1) for r in t2]

        return (t1_new, t2_new)

    # t1: list of first team's players' ratings
    # t2: list of seconds team's players' ratings
    #
    # returns a tuple of two numbers, each number representing team's elo rating
    # team's elo rating is calculated as average rating of all players in given team
    def teams_ratings(self, t1, t2):
        return (sum(t1)/len(t1), sum(t2)/len(t2))

    # K_FACTOR: value the K_FACTOR should be set to
    # default value of K_FACTOR is 32
    def set_k_factor(self, K_FACTOR):
        self.K_FACTOR = K_FACTOR

    # returns the K_FACTOR's current value
    def get_k_factor(self):
        return self.K_FACTOR

    def train(self, tr):
        total_best = (0, 0, 0)
        for i in range(10):
            x, y = 10, 400
            temperature = 10000
            cooling_rate = 0.03
            best = (self.fitness(tr, x, y), x, y)
            explore = best
            seed()

            while temperature > 1:
                x_new, y_new = self.mutate(x, y)
                fitness_new = self.fitness(tr, x_new, y_new)

                if self.acceptance_probability(explore[0], fitness_new, temperature) > random():
                    explore = (fitness_new, x_new, y_new)

                if explore[0] > best[0]:
                    best = explore

                temperature = temperature*(1-cooling_rate)

            if best[0] > total_best[0]:
                total_best = best
            
        print("x: {}, y: {}, fitness: {}".format(total_best[1], total_best[2], total_best[0])) 
        return (total_best[1], total_best[2])

    def predict_trained(self, team1, team2, x, y):
        r_t1, r_t2 = self.teams_ratings(team1, team2)
        return 1.0/(1+x**((r_t2 - r_t1)/y))

    def mutate(self, x, y):
        return (abs(normalvariate(x, sqrt(sqrt(x)))), abs(normalvariate(y, sqrt(sqrt(y)))))

    def acceptance_probability(self, fitness, new_fitness, temperature):
        if new_fitness > fitness:
            return 1

        return exp((new_fitness - fitness)/temperature)

    def fitness(self, tr, x, y):
        e_f = lambda r_t1, r_t2, x, y: 1.0/(1+x**((r_t2 - r_t1)/y))
        fitness = 0

        for tr_i in tr:
            r_t1, r_t2 = self.teams_ratings(tr_i[0], tr_i[1])
            e = e_f(r_t1, r_t2, x, y)

            if e > 0.6 and tr_i[2] == 1 or e < 0.4 and tr_i[2] == 0 or e <= 0.6 and e >= 0.4 and tr_i[2] == 0.5:
                    fitness += 1

        return fitness/len(tr)