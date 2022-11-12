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
        n.adjNode = self.adjNode
        return n

    def make_copy_fresh(self):
        return Node(self.name, self.x, self.y)

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
        self.path = []

    def add_node(self, node):
        self.nodes[node.name] = node

    def add_edge(self, u, v, cost):
        node_u = self.nodes[u]
        node_v = self.nodes[v]
        node_v.update_cost(cost)
        node_u.add_adjNode(node_v)

    # A* Search 
    def a_star(self, start, goal):
        for node in self.nodes.values():
            node.h = node.euclidean(goal)

        q = PriorityQueue()
        start.f = start.h
        start.cost = 0
        start.update_parent(None)
        q.put(start)

        while not q.empty():
            curr = q.get()
            if curr.name == goal.name:
                while curr is not None:
                    self.path.append(curr)
                    curr = curr.parent
                return True

            # print(f'curr: {curr.name} {curr.f} -> ', end='')
            for neighbor in curr.adjNode:
                nn = neighbor.make_copy()
                nn.update_parent(curr)
                nn.update_cost(curr.cost + neighbor.cost)
                nn.f = nn.cost + nn.h
                q.put(nn)
                # print(nn.name, nn.f)
        return False

    def print_path(self):
        n = len(self.path)
        print('Solution path', end=' ')
        for i in range(n):
            node = self.path.pop()
            print(node.name, end='')
            if i != n-1:
                print('-', end='')
        print('\nSolution cost', node.cost)

    def print_graph(self):
        for node in self.nodes.values():
            print(node.name, end=' -> ')
            for adj in node.adjNode:
                print(adj.name, end=' ')
            print()



if __name__ == '__main__':
    graph = Graph()

    # read input from file
    f = open('input.txt')
    n = int(f.readline())
    for i in range(n):
        name, x, y = f.readline().strip().split()
        graph.add_node(Node(name, int(x), int(y)))
    n = int(f.readline())
    for i in range(n):
        u, v, cost = f.readline().strip().split()
        graph.add_edge(u, v, int(cost))


    # get start and goal node
    start = f.readline().strip()
    goal = f.readline().strip()

    start = graph.nodes[start]
    goal = graph.nodes[goal]

    # graph.print_graph()
    result = graph.a_star(start, goal)
    if result:
        graph.print_path()
    else:
        print('No path found')
    
    # graph.print_graph()
    # graph.print_path()
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
    # else:
    #     print('Solution path', end=' ')
    #     graph.print_path()
    #     print('Solution cost', end=' ')
    #     print(graph.get_cost)
