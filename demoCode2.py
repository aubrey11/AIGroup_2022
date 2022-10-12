import sys

def f(node):
    return node.g + node.h

class Queue:
    def __init__(self):
        self.contents = []

    def push(self, node):
        self.contents.append(node)

    def contains(self, x, y):
        for node in self.contents:
            if node.x == x and node.y == y:
                return True
        return False

    def pop(self):
        min = None
        min_index = -1
        for i in range(len(self.contents)):
            if min == None or f(self.contents[i]) < f(min):
                min = self.contents[i]
                min_index = i
        if min == None:
            return None
        else:
            self.contents.pop(min_index)
            return min

    def is_empty(self):
        if len(self.contents) == 0:
            return True
        else:
            return False

class Maze:
    def __init__(self, maze.txt):
        # read file + initialize matrix
        self.matrix = []
        self.dim_x = 0
        self.dim_y = 0
        self.readfile(maze.txt)

    def print(self):
        print("Dims: ", self.dim_y, self.dim_x)
        for row in self.matrix:
            print(row)

    def readfile(self, name):
        f = open(name, "r")
        dim_line = f.readline()
        dims = [int(v) for v in dim_line.split()]
        self.dim_y, self.dim_x = dims[0], dims[1]
        lines = f.readlines()
        for line in lines:
            self.matrix.append([int(val) for val in line.split()])


    def blocked(self, x, y):
        return (self.matrix[y][x] == 0)

def in_range(coordinates, maze):
    if coordinates[0] < 0 or coordinates[0] >= maze.dim_x or coordinates[1] < 0 or coordinates[1] >= maze.dim_y:
        return False
    return True

def manhattan_distance(node, x, y):
    a = abs(node.x - x)
    b = abs(node.y - y)
    return 0

def cell_number(node, maze):
    x = node.x
    y = node.y
    return (y * maze.dim_x) + x + 1

class Node:
    def __init__(self, x, y, maze):
        self.x = x
        self.y = y
        self.g = manhattan_distance(self, 0, 0)  # manhattan distance from source
        self.h = manhattan_distance(self, maze.dim_x-1, maze.dim_y-1)   # manhattan distance to goal
        self.children = []
        self.parent = None

class Solver:
    def __init__(self, maze):
        self.maze = maze

    def trace_path(self, node):
        path = []
        cu = node
        while cu is not None:
            path = [cu] + path
            cu = cu.parent
        return ' '.join(str(cell_number(i, self.maze)) for i in path)

    def solution(self):
        r = self.solve()
        if r is not None:
            print("Solution found")
            return self.trace_path(r)
        else:
            print("No solution found")
            return "No Solution"

    def solve(self):
        node_cu = None
        start = Node(0,0, self.maze)
        q = Queue()
        explored = []
        q.push(start)

        while not q.is_empty():
            node_cu = q.pop()
            if node_cu.x == (self.maze.dim_x - 1) and node_cu.y == (self.maze.dim_y-1):
                # sol found
                break
            # generate neighbor coordinates (left, down, right, up)
            possible_children = [(node_cu.x - 1, node_cu.y),
                                 (node_cu.x, node_cu.y - 1),
                                 (node_cu.x + 1, node_cu.y),
                                 (node_cu.x, node_cu.y +1)]
            # insert valid children into q
            for pair in possible_children:
                # if valid move (not already visited + not explored + not blocked)_
                if in_range(pair, self.maze) and not q.contains(*pair) and not self.maze.blocked(*pair) and pair not in explored:
                    child = Node(*pair, self.maze)
                    child.parent = node_cu
                    q.push(child)
                    node_cu.children.append(child)
                    # ignore check to see if state exists in q or explored w/lower g
                    # since manhattan distance from source will always be the same for same coordinates
            explored.append((node_cu.x, node_cu.y))
        if node_cu is None or node_cu.x != (self.maze.dim_x-1) or node_cu.y != (self.maze.dim_y-1):
            return None
        else:
            return node_cu


def main():
    ''' Program to execute A* search on matrix defined in text file
    names of input and output file should be passed to main as commandline arguments
    ex call:
        main.py input.text output.txt
    '''
    if (len(sys.argv) != 3):
        print('Usage: main.py <input file name> <output file name>\n\tex: main.py input.txt output.txt')
        return
    else:
        input_name, output_name = sys.argv[1], sys.argv[2]
    print('Conducting A* search on input file (' + input_name + ')')
    m = Maze(input_name) # maze class which reads input file into maze matrix
    m.print()
    s = Solver(m) # Solver class which conducts A* search on maze m
    sol = s.solution() # returns solution (or lack thereof) as a string
    outfile = open(output_name, 'w')
    outfile.write(sol)

if __name__ == "__main__":
    main()
