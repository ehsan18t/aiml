import random
import math

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
        return self.manhattan_distance()

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

    def random_child(self):
        children = self.child_states()
        return children[random.randrange(len(children))]

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


def schedule(t):
    if t > 300 : return 0
    return 300 - t


def simulated_annealing(initial):
    chosen_states = []

    # Start by initializing the current state with the initial state
    current_state = initial.copy()

    for t in range(1,301):
        T = schedule(t)
        if(T==0 or current_state.heuristic()==0):
            return chosen_states, t

        random_state = current_state.random_child()

        # Check if neighbor is best so far
        del_E = current_state.heuristic() - random_state.heuristic()

        # if the new solution is better, accept it
        if del_E >= 0:
            current_state = random_state
            chosen_states.append(current_state)
        # if the new solution is not better, accept it with a probability of e^(-cost/temp)
        else:
            p = math.exp(del_E/T)
            if(random.random() <= p):
                current_state = random_state
                chosen_states.append(current_state)


def main():
    # input from file
    f = open('input.txt')
    initial = State()
    for line in f.readlines():
        initial.grid.append([int(x) for x in line.split()])

    # simulated annealing
    selected_states, itr = simulated_annealing(initial)
    solution = selected_states[-1]

    # output
    print('Selected States:')
    for state in selected_states:
        print(state, 'h =', state.heuristic())

    print('\nIterations:', itr)
    print(solution, 'h =', solution.heuristic())


main()