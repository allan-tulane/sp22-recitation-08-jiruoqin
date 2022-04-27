from cgitb import reset
from collections import defaultdict
from functools import reduce 

def make_undirected_graph(edge_list):
    """ Makes an undirected graph from a list of edge tuples. """
    graph = defaultdict(set)
    for e in edge_list:
        graph[e[0]].add(e[1])
        graph[e[1]].add(e[0])
    return graph


def reachable(graph, start_node):
    """
    Returns:
      the set of nodes reachable from start_node
    """
    #result = set([start_node])
    frontier = set([start_node])
    visited = set()
    def reach(visited, frontier):
        if len(frontier) == 0:
            return visited 
        else:
            visited_new = visited | frontier
            visited = visited_new
            frontier_neighbors = reduce(set.union, [graph[f] for f in frontier])
            frontier = frontier_neighbors - visited
        return reach(visited, frontier)
        
    return reach(visited, frontier)

def test_reachable():
    graph = make_undirected_graph([('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'B')])
    assert sorted(reachable(graph, 'A')) == ['A', 'B', 'C', 'D']

    graph = make_undirected_graph([('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'B'), ('E', 'F'), ('F', 'G')])
    assert sorted(reachable(graph, 'A')) == ['A', 'B', 'C', 'D']
    assert sorted(reachable(graph, 'E')) == ['E', 'F', 'G']




def connected(graph):
    start_ndoe = next(iter(graph))
    reachable_set = reachable(graph, start_ndoe)
    all_nodes = graph.keys()
    for n in all_nodes:
        if n not in reachable_set:
            return False
    
    return True 

def test_connected():
    graph = make_undirected_graph([('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'B')])
    assert connected(graph) == True
    graph = make_undirected_graph([('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'B'), ('E', 'F'), ('F', 'G')])
    assert connected(graph) == False



def n_components(graph):
    """
    Returns:
      the number of connected components in an undirected graph
    """
    all_nodes = list(graph.keys())
    count = 0
    while len(all_nodes) != 0:
        start_ndoe = all_nodes[0]
        reachable_set = reachable(graph, start_ndoe)
        count += 1
        all_nodes = list(set(all_nodes).difference(reachable_set))
    
    return count 

def test_n_components():
    graph = make_undirected_graph([('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'B')])
    assert n_components(graph) == 1

    graph = make_undirected_graph([('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'B'), ('E', 'F'), ('F', 'G')])
    assert n_components(graph) == 2
