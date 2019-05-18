from collections import defaultdict
from country import countries_links


class Graph:

    def __init__(self):
        self.graph = defaultdict(list)
        self.path_cost = dict()
        self.paths = []

    def add_edge(self, u, v, cost):
        self.graph[u].append(v)
        new_distance = {}
        if u in self.path_cost:
            new_distance = self.path_cost[u]
        new_distance[v] = cost
        self.path_cost[u] = new_distance

    def calc_all_paths(self, u, d, visited, path):
        # Mark the current node as visited and store in path
        visited.add(u)
        path.append(u)

        # If current vertex is same as destination, then append path to paths
        if u == d:
            total_cost = 0
            for i in range(len(path)-1):
                total_cost += self.get_cost(path[i], path[i+1])

            new_path = []
            for i in range(len(path)):
                new_path.append(path[i])

            new_path.append(total_cost)
            self.paths.append(new_path)
        else:
            # If current vertex is not destination
            # Recur for all the vertices adjacent to this vertex
            for i in self.graph[u]:
                if i not in visited:
                    self.calc_all_paths(i, d, visited, path)

        # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited.remove(u)

    def get_all_paths(self, s, d):
        self.paths = []
        # Mark all the vertices as not visited
        visited = set()
        path = []
        # Call the recursive helper function to calculate all paths
        self.calc_all_paths(s, d, visited, path)
        return self.paths

    def get_cost(self, u, v):
        return self.path_cost[u][v]


g = Graph()


def add_edges(routes):
    global g
    for route in routes:
        g.add_edge(route[0], route[1], route[2])


add_edges(countries_links)


def get_paths(src, dest):
    global g
    rslt = g.get_all_paths(src, dest)
    print(rslt)
    print("hi")
    rslt.sort(key=lambda x: x[-1])
    return rslt
