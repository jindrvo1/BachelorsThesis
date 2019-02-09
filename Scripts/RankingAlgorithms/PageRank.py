import numpy as np

# TODO: DIVISION BY ZERO HANDLING

def func_0(args):
    return args['edge'].teams[args['node_to']]['won']/float(args['edge'].games_total)*1.0/(args['max_games']-args['edge'].games_total+1)    

def func_1(args):
    return args['edge'].teams[args['node_to']]['won']/float(args['edge'].games_total)

def func_2(args):
    if args['edge'].teams[args['node_to']]['score']+args['edge'].teams[args['node_from']]['score'] == 0:
        return 0
    else:
        return args['edge'].teams[args['node_to']]['won']/float(args['edge'].games_total)+float(args['edge'].teams[args['node_to']]['score'])/(args['edge'].teams[args['node_to']]['score']+args['edge'].teams[args['node_from']]['score'])

def func_3(args):
    return args['edge'].teams[args['node_to']]['won']

def func_4(args):
    if args['edge'].teams[args['node_from']]['score'] == 0:
        return 0
    else:
        return args['edge'].teams[args['node_to']]['score']/float(args['edge'].teams[args['node_from']]['score'])

def func_5(args):
    if args['edge'].teams[args['node_from']]['won'] == 0:
        return 0
    else:
        return args['edge'].teams[args['node_to']]['won']/float(args['edge'].teams[args['node_from']]['won'])

def func_6(args):
    return args['edge'].teams[args['node_to']]['won']/float(args['edge'].games_total)+0.5*(args['edge'].games_total-args['edge'].teams[args['node_to']]['won']-args['edge'].teams[args['node_from']]['won'])/float(args['edge'].games_total)

def func_7(args):
    if args['edge'].teams[args['node_to']]['score']+args['edge'].teams[args['node_from']]['score'] == 0:
        return 0
    else:
        return float(args['edge'].teams[args['node_to']]['score'])/(args['edge'].teams[args['node_to']]['score']+args['edge'].teams[args['node_from']]['score'])

def func_8(args):
    return args['edge'].teams[args['node_to']]['score']/float(args['edge'].games_total)

def func_9(args):
    return args['edge'].teams[args['node_to']]['score']

class PageRank(object):
    def __init__(self, d = 0.15):
        self.graph = Graph()
        self.d = d
        self.functions = [func_0, func_1, func_2, func_3, func_4, func_5, func_6, func_7, func_8, func_9]

    # if there is already an edge between t1 and t2, calls add_match() to add another match to the existing edge
    # otherwise, creates a new edge
    def add_match(self, t1, t2, s1, s2):
        self.graph.add_node(t1)
        self.graph.add_node(t2)

        edge = self.graph.get_edge(t1, t2)
        if edge is None:
            new_edge = Edge(t1, t2, s1, s2, 1, 1 if s1 > s2 else 0, 1 if s2 > s1 else 0)
            self.graph.add_edge(t1, t2, new_edge)
        else:
            edge.add_match(t1, t2, s1, s2)

    def __str__(self):
        ret = ""
        for edges in self.graph.edges.values():
            for edge in edges.values():
                for team, stats in edge.teams.items():  
                    ret += "{}: ".format(team)
                    for key, stat in stats.items():
                        ret += "{} {} ".format(key, stat)
                    ret += "\n"
                ret += "total number of games: {}\n\n".format(edge.games_total)
        return ret

    def calculate_pagerank(self, weighting_function = 0):
        A = [[0 for x in range(len(self.graph.edges))] for y in range(len(self.graph.edges))]
        team_indexes = {}
        index = 0
        for node in self.graph.edges:
            team_indexes[node] = index
            index += 1
        
        max_games = 0

        for edges in self.graph.edges.values():
            for edge in edges.values():
                if edge.games_total > max_games:
                    max_games = edge.games_total

        for node_from, edges in self.graph.edges.items():
            for node_to, edge in edges.items():
                function_args = {'max_games': max_games, 'edge': edge, 'node_to': node_to, 'node_from': node_from}
                A[team_indexes[node_from]][team_indexes[node_to]] = 0
                A[team_indexes[node_from]][team_indexes[node_to]] = self.functions[weighting_function](function_args)

        Q = [[0 for x in range(len(A))] for y in range(len(A))]

        for i in range(len(A)):
            for j in range(len(A)):
                if sum(A[i]) == 0:
                    Q[i][j] = 0
                else:
                    Q[i][j] = (1-self.d)*A[i][j]/sum(A[i])+self.d/len(A)    

        Q = np.array(Q)
        v = np.array([1.0/len(A) for x in range(len(A))])

        prev_v = v
        v = v.dot(Q)
        
        while any([abs(x)>0.000001 for x in prev_v-v]):
            prev_v = v
            v = v.dot(Q)
        
        results = {}        
        for team_name, team_index in team_indexes.items():
            results[team_name] = v[team_index]

        return results

class Graph(object):
    def __init__(self):
        self.edges = {}

    # adds a new node
    def add_node(self, node):
        if node not in self.edges:
            self.edges[node] = None

    # adds an edge to both t1's and t2's dictionaries of edges
    def add_edge(self, t1, t2, edge):
        if self.edges[t1] is None:
            self.edges[t1] = {t2: edge}
        else:
            self.edges[t1][t2] = edge

        if self.edges[t2] is None:
            self.edges[t2] = {t1: edge}
        else:
            self.edges[t2][t1] = edge

    # if an edge exists between t1 and t2, it is returned
    # otherwise, None is returned
    def get_edge(self, t1, t2):
        if t1 in self.edges and self.edges[t1] is not None:
            if t2 in self.edges[t1]:
                return self.edges[t1][t2]
        else:
            return None

# an edge between two teams t1 and t2
# instead of weight, the edge carries information about the teams' relation
# the information (team's score and number of games won against the other team) is stored in a dictionary with team's name as a key
# variable games_total carries the information of all games played between the teams        
class Edge(object):
    def __init__(self, t1, t2, score_t1, score_t2, games_total, games_won_t1, games_won_t2):
        self.teams = {}
        self.teams[t1] = {'score': score_t1, 'won': games_won_t1}
        self.teams[t2] = {'score': score_t2, 'won': games_won_t2}
        self.games_total = games_total

    # function used to add another match's result to an existing edge
    def add_match(self, t1, t2, score_t1, score_t2):
        self.teams[t1]['score'] += score_t1
        self.teams[t2]['score'] += score_t2
        self.games_total += 1
        if score_t1 > score_t2:
            self.teams[t1]['won'] += 1
        elif score_t1 < score_t2:
            self.teams[t2]['won'] += 1
