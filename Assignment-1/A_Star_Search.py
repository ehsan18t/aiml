import math
from queue import PriorityQueue

class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.parent = None
        self.x = x
        self.y = y
        self.cost = 0   # edge cost so far
        self.h = 0      # heuristic cost
        self.f = 0      # f = g + h
        self.adjNode = []

    def update_parent(self, parent):
        self.parent = parent

    def update_cost(self, cost):
        self.cost = cost

    def add_adjNode(self, node):
        self.adjNode.append(node)

    def make_copy(self):
        n = Node(self.name, self.x, self.y)
        n.h = self.h
        n.f = self.f
        n.adjNode = self.adjNode
        return n

    def euclidean(self, d2):
        return math.sqrt((self.x - d2.x)**2 + (self.y - d2.y)**2)

    def __lt__(self, o):
        return self.f < o.f

    def __eq__(self, o):
        return self.f == o.f

    def __str__(self):
        return f'{self.name} {self.x} {self.y}'

class Graph:
    def __init__(self):
        self.nodes = {}
        self.costs = {}
        self.path = []
        self.goal = None
        self.start = None

    def read_input(self, file):
        f = open(file)
        n = int(f.readline())
        for i in range(n):
            name, x, y = f.readline().strip().split()
            self.add_node(Node(name, int(x), int(y)))
        n = int(f.readline())
        for i in range(n):
            u, v, cost = f.readline().strip().split()
            self.add_edge(u, v, int(cost))

        # get start and goal node
        start = f.readline().strip()
        goal = f.readline().strip()
        self.start = self.nodes[start]
        self.goal = self.nodes[goal]

    def add_node(self, node):
        self.nodes[node.name] = node

    def add_edge(self, u, v, cost):
        node_u = self.nodes[u]
        node_v = self.nodes[v]
        node_u.add_adjNode(node_v)
        self.costs[f'{u}-{v}'] = cost

    def calculate_heuristic(self, d2):
        for node in self.nodes.values():
            node.h = node.euclidean(d2)

    def get_edge_cost(self, u, v):
        return self.costs[f'{u.name}-{v.name}']

    # A* Search implementation
    def a_star_search(self, start, goal):
        self.calculate_heuristic(goal)

        q = PriorityQueue()
        start.cost = 0
        start.f = start.h
        start.update_parent(None)
        q.put(start)

        while not q.empty():
            curr = q.get()
            if curr.name == goal.name:
                while curr is not None:
                    self.path.append(curr)
                    curr = curr.parent
                return True

            for neighbor in curr.adjNode:
                nn = neighbor.make_copy()
                nn.update_parent(curr)
                nn.update_cost(curr.cost + self.get_edge_cost(curr, nn))
                nn.f = nn.cost + nn.h
                q.put(nn)
        return False

    def print_path(self):
        n = len(self.path)
        print('Path:', end=' ')
        for i in range(n):
            node = self.path.pop()
            print(node.name, end='')
            if i != n-1:
                print(' -> ', end='')
        print('\nCost:', node.cost)

    def print_graph(self):
        for node in self.nodes.values():
            print(node.name, end=' -> ')
            for adj in node.adjNode:
                print(adj.name, end=' ')
            print()


def main():
    graph = Graph()

    # read input from file
    graph.read_input('input.txt')

    # A* Search Output
    # graph.print_graph()
    if graph.a_star_search(graph.start, graph.goal):
        graph.print_path()
    else:
        print('No path found')


# main call
main()