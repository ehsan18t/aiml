class State:
    def __init__(self):
        self.grid = []
        self.cost = 0   # cumulative cost

    def misplaced_tiles(self):
        cost = 0
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] != (3 * i) + j:
                    cost += 1
        return cost

    def manhattan_distance(self):
        cost = 0
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] != (3 * i) + j and self.grid[i][j] != 0:
                    cost += abs(i - (self.grid[i][j] // 3)) + abs(j - (self.grid[i][j] % 3))
        return cost

    def heuristic(self):
        return self.misplaced_tiles()

    def child_states(self):
        children = []
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == 0:
                    break
            else:
                continue
            break

        if i > 0:
            child = self.copy()
            child.grid[i][j] = child.grid[i - 1][j]
            child.grid[i - 1][j] = 0
            child.cost += 1
            children.append(child)

        if i < 2:
            child = self.copy()
            child.grid[i][j] = child.grid[i + 1][j]
            child.grid[i + 1][j] = 0
            child.cost += 1
            children.append(child)

        if j > 0:
            child = self.copy()
            child.grid[i][j] = child.grid[i][j - 1]
            child.grid[i][j - 1] = 0
            child.cost += 1
            children.append(child)

        if j < 2:
            child = self.copy()
            child.grid[i][j] = child.grid[i][j + 1]
            child.grid[i][j + 1] = 0
            child.cost += 1
            children.append(child)

        return children

    def best_child(self):
        children = self.child_states()
        # sort children by heuristic
        children.sort(key=lambda x: x.heuristic())
        return children[0]


    def copy(self):
        new_state = State()
        new_state.grid = [row[:] for row in self.grid]
        new_state.cost = self.cost
        return new_state

    def __eq__(self, __o: object) -> bool:
        return self.grid == __o.grid

    def __lt__(self, __o: object) -> bool:
        return self.cost < __o.cost

    def __str__(self) -> str:
        return str(self.grid)


def hill_climbing(initial, goal):
    current = initial.copy()
    iteration = 0
    while True:
        best = current.best_child()
        print('Neighbor =', best,'h =' , best.heuristic())
        iteration += 1
        if current.heuristic() <= best.heuristic():
            break
        else:
            current = best
    print('\nsolution =', current ,'h =', current.heuristic())
    print('Iteration =', iteration)


def main():
    goal = State()
    goal.grid = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

    # input from file
    f = open('input.txt')
    initial = State()
    for line in f.readlines():
        initial.grid.append([int(x) for x in line.split()])

    hill_climbing(initial, goal)


main()