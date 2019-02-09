from RankingAlgorithms import PageRank

pr = PageRank()

pr.add_match('A', 'B', 4, 2)
pr.add_match('A', 'B', 4, 2)
pr.add_match('A', 'B', 1, 5)
pr.add_match('A', 'C', 3, 2)
pr.add_match('A', 'C', 3, 1)
pr.add_match('A', 'C', 1, 5)
pr.add_match('A', 'D', 1, 0)
pr.add_match('A', 'D', 5, 3)
pr.add_match('A', 'D', 3, 1)
pr.add_match('C', 'B', 3, 1)
pr.add_match('C', 'B', 3, 2)
pr.add_match('C', 'B', 2, 1)
pr.add_match('D', 'B', 2, 1)
pr.add_match('D', 'B', 2, 1)
pr.add_match('D', 'B', 2, 1)
pr.add_match('D', 'C', 2, 1)
pr.add_match('D', 'C', 2, 1)
pr.add_match('D', 'C', 0, 1)

for i in [0,1,2,3,4,7,8,9]:
	print(i)
	pr.calculate_pagerank(i)