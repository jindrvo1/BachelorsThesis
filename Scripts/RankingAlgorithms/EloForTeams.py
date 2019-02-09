"""
In this approach, I change only the x and y parameters and I do that after rating players on the training set.
Training is done using the cross-entropy method.

~505/1520 correctly classified.
"""

from math import exp, sqrt, log
from random import seed, random, normalvariate
import numpy as np
from scipy.stats import norm

class EloForTeams(object):
    def __init__(self, k_factor = 32, distribution = "logistics", sigma = 2000/7, x = 10, y = 400):
        self.k_factor = k_factor
        self.distribution = distribution
        self.sigma = sigma
        self.x = x
        self.y = y

    # t1: list of first team's players' ratings
    # t2: list of seconds team's players' ratings
    #
    # returns a tuple of two numbers representing each team's expectancy to win
    def predict_winner(self, t1, t2):
        r_t1, r_t2 = self.teams_ratings(t1, t2)

        if self.distribution == "normal":
            d1 = norm(r_t1, self.sigma)
            d2 = norm(r_t2, self.sigma)
            intersect = (d1.mean() + d2.mean())/2
            e_t1 = d1.sf(intersect)
            e_t2 = d2.sf(intersect)
        else:
            e_t1 = 1.0/(1+self.x**((r_t2-r_t1)/self.y))
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
    def rate_match(self, t1, t2, s_t1, s_t2 = None):
        if s_t2 is None:
            s_t2 = 1 - s_t1

        r_t1, r_t2 = self.teams_ratings(t1, t2)
        e_t1, e_t2 = self.predict_winner(t1, t2)

        r_t1_new = r_t1 + self.k_factor*(s_t1-e_t1)
        r_t2_new = r_t2 + self.k_factor*(s_t2-e_t2)

        t1_new = [r + (r_t1_new-r_t1)*((r_t1_new-(2*s_t1-1)*(r-r_t1))/(r_t1_new)) for r in t1]
        t2_new = [r + (r_t2_new-r_t2)*((r_t2_new-(2*s_t2-1)*(r-r_t2))/(r_t2_new)) for r in t2]

        return (t1_new, t2_new)

    # t1: list of first team's players' ratings
    # t2: list of seconds team's players' ratings
    #
    # returns a tuple of two numbers, each number representing team's elo rating
    # team's elo rating is calculated as average rating of all players in given team
    def teams_ratings(self, t1, t2):
        return (sum(t1)/len(t1), sum(t2)/len(t2))

    def CEM_train(self, tr):
        if self.distribution == "normal":
            return self.CEM_train_normal(tr)
        else:
            return self.CEM_train_logistic(tr)

    def CEM_train_normal(self, tr):
        N_SAMPLES = 100
        ELITE_PERCENTAGE = 0.2
        N_ITERATIONS = 100
        N_PARAMETERS = 1
        x = self.sigma

        mu = np.array([x])
        sigma = np.array([1])
        
        for it in range(N_ITERATIONS):
            candidates = np.random.normal(mu, sigma, (N_SAMPLES, N_PARAMETERS))
            fitnesses = [self.CEM_fitness(tr, candidate[0]) for candidate in candidates]
            n_elite = int(ELITE_PERCENTAGE*N_SAMPLES)
            elite_inds = np.argsort(fitnesses)[N_SAMPLES - n_elite:N_SAMPLES]
            elite = [candidates[i] for i in elite_inds]
            mu = np.mean(elite, axis=0)
            sigma = np.std(elite, axis=0)
        
        return mu[0]

    def CEM_train_logistic(self, tr):
        N_SAMPLES = 100
        ELITE_PERCENTAGE = 0.2
        N_ITERATIONS = 100
        N_PARAMETERS = 2
        x, y = self.x, self.y

        mu = np.array([x, y])
        sigma = np.array([1, 1])
        
        for it in range(N_ITERATIONS):
            candidates = np.random.normal(mu, sigma, (N_SAMPLES, N_PARAMETERS))
            fitnesses = [self.CEM_fitness(tr, candidate[0], candidate[1]) for candidate in candidates]
            n_elite = int(ELITE_PERCENTAGE*N_SAMPLES)
            elite_inds = np.argsort(fitnesses)[N_SAMPLES - n_elite:N_SAMPLES]
            elite = [candidates[i] for i in elite_inds]
            mu = np.mean(elite, axis=0)
            sigma = np.std(elite, axis=0)
        
        return (mu[0], mu[1])

    def CEM_fitness(self, tr, x, y = 0):
        if self.distribution == "normal":
            return self.CEM_fitness_normal(tr, x)
        else:
            return self.CEM_fitness_logistic(tr, x, y)

    def CEM_fitness_normal(self, tr, x):
        e = 0
        for tr_i in tr:
            p_t1, p_t2 = self.CEM_predict_trained(tr_i[0], tr_i[1], x)
            o = tr_i[2]
            e += o*log(p_t1)+(1-o)*log(p_t2)
        e /= -len(tr)
        return e

    def CEM_fitness_logistic(self, tr, x, y):
        e = 0
        for tr_i in tr:
            p_t1, p_t2 = self.CEM_predict_trained(tr_i[0], tr_i[1], x, y)
            o = tr_i[2]
            e += o*log(p_t1)+(1-o)*log(p_t2)
        e /= -len(tr)
        return e

    def CEM_predict_trained(self, t1, t2, sigma = None, x = None, y = None):
        if self.distribution == "normal":
            return self.CEM_predict_trained_normal(t1, t2, sigma)
        else:
            return self.CEM_predict_trained_logistic(t1, t2, x, y)

    def CEM_predict_trained_normal(self, t1, t2, x):
        r_t1, r_t2 = self.teams_ratings(t1, t2)

        d1 = norm(r_t1, x)
        d2 = norm(r_t2, x)
        intersect = (r_t1 + r_t2)/2

        e1 = d1.sf(intersect)
        e2 = 1 - e1

        return (e1, e2)

    def CEM_predict_trained_logistic(self, t1, t2, x, y):
        r_t1, r_t2 = self.teams_ratings(t1, t2)

        e_t1 = 1.0/(1+x**((r_t2-r_t1)/y))
        e_t2 = 1-e_t1

        return (e_t1, e_t2)

    def SA_train(self, tr):
        if self.distribution == "normal":
            return self.SA_train_normal(tr)
        else:
            return self.SA_train_logistics(tr)

    def SA_train_logistics(self, tr):
        x, y = self.x, self.y
        temperature = 10000
        cooling_rate = 0.03
        best = (self.SA_log_likelihood(tr, x, y), x, y)
        explore = best
        seed()

        while temperature > 1:
            x_new, y_new = self.SA_mutate(x, y)
            fitness_new = self.SA_log_likelihood(tr, x_new, y_new)

            if self.SA_acceptance_probability(explore[0], fitness_new, temperature) > random():
                explore = (fitness_new, x_new, y_new)

            if explore[0] < best[0]:
                best = explore

            temperature = temperature*(1-cooling_rate)
            
        return (best[1], best[2])

    def SA_predict_trained(self, t1, t2, sigma = None, x = None, y = None):
        if self.distribution == "normal":
            return self.SA_predict_trained_normal(t1, t2, sigma)
        else:
            return self.SA_predict_trained_logistics(t1, t2, x, y)

    def SA_predict_trained_logistics(self, team1, team2, x, y):
        r_t1, r_t2 = self.teams_ratings(team1, team2)
        
        e1 = 1.0/(1+x**((r_t2 - r_t1)/y))
        e2 = 1-e1

        return (e1, e2)

    def SA_predict_trained_normal(self, team1, team2, x):
        r_t1, r_t2 = self.teams_ratings(team1, team2)

        d1 = norm(r_t1, x)
        d2 = norm(r_t2, x)
        intersect = (r_t1 + r_t2)/2

        e1 = d1.sf(intersect)
        e2 = 1 - e1

        return (e1, e2)

    def SA_mutate(self, x, y = 0):
        if self.distribution == "normal":
            return abs(normalvariate(x, sqrt(sqrt(x))))
        else:
            return (abs(normalvariate(x, sqrt(sqrt(x)))), abs(normalvariate(y, sqrt(sqrt(y)))))

    def SA_acceptance_probability(self, fitness, new_fitness, temperature):
        if new_fitness < fitness:
            return 1

        return exp((fitness - new_fitness)/temperature)

    def SA_log_likelihood(self, tr, x, y = 0):
        if self.distribution == "normal":
            return self.SA_log_likelihood_normal(tr, x)
        else:
            return self.SA_log_likelihood_logistics(tr, x, y)
    
    def SA_log_likelihood_logistics(self, tr, x, y):
        e_f = lambda r_t1, r_t2, x, y: 1.0/(1+x**((r_t2 - r_t1)/y))
        log_likelihood = 0

        for tr_i in tr:
            r_t1, r_t2 = self.teams_ratings(tr_i[0], tr_i[1])
            e = e_f(r_t1, r_t2, x, y)

            w = 1 if tr_i[2] == 1 else 0
            log_likelihood += w*log(e) + (1-w)*log(1-e)

        log_likelihood /= -len(tr)

        return log_likelihood

    def SA_train_normal(self, tr):
        x = self.sigma
        temperature = 10000
        cooling_rate = 0.03
        best = (self.SA_log_likelihood(tr, x), x)
        explore = best
        seed()

        while temperature > 1:
            x_new = self.SA_mutate(x)
            fitness_new = self.SA_log_likelihood(tr, x_new)

            if self.SA_acceptance_probability(explore[0], fitness_new, temperature) > random():
                explore = (fitness_new, x_new)

            if explore[0] < best[0]:
                best = explore

            temperature = temperature*(1-cooling_rate)

        return best[1]

    def SA_log_likelihood_normal(self, tr, x):
        log_likelihood = 0

        for tr_i in tr:
            r_t1, r_t2 = self.teams_ratings(tr_i[0], tr_i[1])
            d1 = norm(r_t1, x)
            d2 = norm(r_t2, x)
            intersect = (d1.mean() + d2.mean())/2

            e = d1.sf(intersect)

            w = 1 if tr_i[2] == 1 else 0
            log_likelihood += w*log(e) + (1-w)*log(1-e)

        log_likelihood /= -len(tr)

        return log_likelihood

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
