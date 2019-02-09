"""
In this approach, I change only the x and y parameters and I do that after rating players on the training set.
Training is done using the cross-entropy method.

~505/1520 correctly classified.
"""

from math import exp, sqrt, log
from random import seed, random, normalvariate
import numpy as np

class EloForTeams(object):
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
		N_SAMPLES = 100
		ELITE_PERCENTAGE = 0.2
		N_ITERATIONS = 100
		N_PARAMETERS = 2
		x, y = 10, 400

		mu = np.array([x, y])
		sigma = np.array([1, 1])
		
		for it in range(N_ITERATIONS):
			candidates = np.random.normal(mu, sigma, (N_SAMPLES, N_PARAMETERS))
			fitnesses = [self.fitness(tr, candidate[0], candidate[1]) for candidate in candidates]
			n_elite = int(ELITE_PERCENTAGE*N_SAMPLES)
			elite_inds = np.argsort(fitnesses)[N_SAMPLES - n_elite:N_SAMPLES]
			elite = [candidates[i] for i in elite_inds]
			mu = np.mean(elite, axis=0)
			sigma = np.std(elite, axis=0)
		
		return (mu[0], mu[1])

	def fitness(self, tr, x, y):
		e = 0
		for tr_i in tr:
			p_t1, p_t2 = self.predict_winner_training(tr_i[0], tr_i[1], x, y)
			o = tr_i[2]
			e += o*log(p_t1)+(1-o)*log(p_t2)
		e /= -len(tr)
		return e

	def predict_winner_training(self, t1, t2, x, y):
		r_t1, r_t2 = self.teams_ratings(t1, t2)

		e_t1 = 1.0/(1+x**((r_t2-r_t1)/y))
		e_t2 = 1-e_t1

		return (e_t1, e_t2)