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

    def euclidean(self, d2):
        return math.sqrt((self.x - d2.x)**2 + (self.y - d2.y)**2)

    def __lt__(self, o):
        return self.cost < o.cost

    def __eq__(self, o):
        return self.name == o.name and self.x == o.x and self.y == o.y and self.cost == o.cost

    def __str__(self):
        return f'{self.name} {self.x} {self.y}'

class Graph:
    def __init__(self):
        self.nodes = {}
        self.path = []

    def add_node(self, node):
        self.nodes[node.name] = node

    def add_edge(self, u, v, cost):
        node_u = self.nodes[u]
        node_v = self.nodes[v]
        node_u.update_cost(cost)
        node_v.update_cost(cost)
        node_u.add_adjNode(node_v)
        # node_v.add_adjNode(node_u)

    # A* Search 
    def a_star(self, start, goal):
        for node in self.nodes.values():
            node.f = node.euclidean(goal)

        start_node = self.nodes[start.name]
        goal_node = self.nodes[goal.name]
        start_node.h = start_node.euclidean(goal_node)
        start_node.f = start_node.h
        queue = PriorityQueue()
        queue.put(start_node)
        while not queue.empty():
            node = queue.get()
            if node.name == goal_node.name:
                self.path.append(node)
                while node.parent is not None:
                    self.path.append(node.parent)
                    node = node.parent
                return self.path
            for adj in node.adjNode:
                print(node, end=' -> ')
                if adj.name == start_node.name or adj.name == node.name:
                    continue
                adj.h = adj.euclidean(goal_node)
                adj.f = node.cost + adj.h
                adj.update_parent(node)
                queue.put(adj)
                print(adj)
        return None


    def print_path(self):
        n = len(self.path)
        for i in range(n):
            node = self.path.pop()
            print(node.name, end='')
            if i != n-1:
                print('-', end='')
        print()

    def get_cost(self):
        return self.path[-1].cost

    def print_graph(self):
        for node in self.nodes.values():
            print(node, end=' -> ')
            for adj in node.adjNode:
                print(adj.name, end=' ')
            print()



if __name__ == '__main__':
    graph = Graph()

    # read input from file
    f = open('input.txt')
    n = int(f.readline())
    for i in range(n):
        name, x, y = f.readline().split()
        graph.add_node(Node(name, int(x), int(y)))
    n = int(f.readline())
    for i in range(n):
        u, v, cost = f.readline().split()
        graph.add_edge(u, v, int(cost))


    # get start and goal node
    start = f.readline().strip()
    goal = f.readline().strip()

    start = graph.nodes[start]
    goal = graph.nodes[goal]

    graph.a_star(start, goal)
    # graph.print_graph()
    graph.print_path()
    # g = graph.nodes[goal.name]
    # while g.name != goal.name:
    #     print(goal.name, end=' -> ')
    #     g = graph.nodes[g.parent.name]
    
    # for node in graph.nodes.values():
    #     if node.name == start.name:
    #         print(node.name, node.cost, node.f, node.h)
    #         continue
    #     print(node.name, node.parent.name , node.cost, node.f, node.h)

    # output
    # if found:
    #     print('No path')
    # else:
    #     print('Solution path', end=' ')
    #     graph.print_path()
    #     print('Solution cost', end=' ')
    #     print(graph.get_cost)
