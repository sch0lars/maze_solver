# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                   #
#   A solution to Q2 on https://aonecode.com/amazon-online-assessment-questions     #
#   with a few example mazes, one with no solution.                                 #
#                                                                                   #
#   Author: Tyler Hooks                                                             #
#                                                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


from collections import deque

class Graph:
    def __init__(self, graph):
        self.graph = graph
        self.dimensions = (len(graph), len(graph[0]))
        self.coordinates = []
        self.source = None
        self.destination = None
        for row in range(len(graph)):
            for column in range(len(graph[row])):
                if graph[row][column] != 'D':
                    self.coordinates.append((row, column))
                if graph[row][column] == 'S':
                    self.source = (row, column)
                if graph[row][column] == 'X':
                    self.destination = (row, column)
        self.neighbors = self.get_neighbors()
        self.solution = self.solve()

    def print_graph(self) -> None:
        for row in self.graph:
            print(row)

    def print_solution(self) -> None:
        graph = self.graph
        source = self.source
        destination = self.destination
        for row in range(len(graph)):
            for column in range(len(graph[row])):
                point = (row, column)
                if point in self.solution and point not in [source, destination]:
                    graph[row][column] = '*'

        for row in graph:
            print(row)
           
    def get_neighbors(self) -> dict:
        coordinates = self.coordinates
        neighbors = {}
        dimensions = self.dimensions
        for point in coordinates:
            neighbors[point] = []
            if point[0] >= 0 and point[0] < dimensions[0] - 1:
                neighbors[point].append((point[0] + 1, point[1]))
            if point[0] > 0 and point[0] <= dimensions[0] - 1:
                neighbors[point].append((point[0] - 1, point[1]))
            if point[1] >= 0 and point[1] < dimensions[1] - 1:
                neighbors[point].append((point[0], point[1] + 1))
            if point[1] > 0 and point[1] <= dimensions[1] - 1:
                neighbors[point].append((point[0], point[1] - 1))
            if point[0] > 0 and point[0] < dimensions[0] - 1 and point[1] > 0 and point[1] < dimensions[1] - 1:
                neighbors[point].append((point[0], point[1] + 1))
                neighbors[point].append((point[0], point[1] - 1))
                neighbors[point].append((point[0] + 1, point[1]))
                neighbors[point].append((point[0] - 1, point[1]))

            # Remove duplicate tuples.
            for key, value in neighbors.items():
                neighbors[key] = list(set(value))

            # Remove nodes that are not in the coordinate list (nodes that have a value of 'D').
            for neighbor, coordinate_list in neighbors.items():
                for c in coordinate_list:
                    if c not in coordinates:
                        neighbors[neighbor].remove(c)
                    
            
        return neighbors
        

    def reconstruct_path(self, prev) -> list:
        path = []
        source = self.source
        destination = self.destination
        current_node = destination
        solution_found = True
        while current_node != source:
            try:
                path.append(current_node)
                current_node = prev[current_node]
            except KeyError:
                solution_found = False
                break
        if solution_found == True:
            path.append(source)
            path.reverse()

        if path[0] == source:
            return path
        return []

    def solve(self) -> list:
        source = self.source
        destination = self.destination
        queue = deque([source])
        vertices = self.coordinates.copy()
        visited = {vertex: False for vertex in vertices}
        prev = {vertex: None for vertex in vertices}

        while queue:
            current_node = queue.popleft()
            if current_node == destination:
                break
            neighbors = self.neighbors[current_node]
            for neighbor in neighbors:
                if not visited[neighbor]:
                    queue.append(neighbor)
                    visited[neighbor] = True
                    prev[neighbor] = current_node
      
        path = self.reconstruct_path(prev)
        
        return path if path else ['No solution']


# Main
if __name__ == "__main__":
    maze = [
                ['S', 'O', 'O', 'O'],
                ['D', 'O', 'D', 'O'],
                ['O', 'O', 'O', 'O'],
                ['X', 'D', 'D', 'O']
            ]
    graph = Graph(maze)
    solution = graph.solution
    print(f'The maze can be solved in {len(solution) - 1} steps.')
    graph.print_solution()
    print(f'Solution: {solution}\n')

    maze = [
                ['O', 'O', 'O', 'O', 'O'],
                ['D', 'S', 'D', 'D', 'O'],
                ['O', 'D', 'D', 'O', 'O'],
                ['O', 'D', 'D', 'O', 'D'],
                ['O', 'X', 'O', 'O', 'D']
            ]
    graph = Graph(maze)
    solution = graph.solution
    print(f'The maze can be solved in {len(solution) - 1} steps.')
    graph.print_solution()
    print(f'Solution: {solution}\n')

    maze = [
                ['S', 'O', 'O', 'O', 'O'],
                ['D', 'O', 'D', 'D', 'O'],
                ['O', 'D', 'D', 'O', 'O'],
                ['O', 'D', 'D', 'D', 'D'],
                ['O', 'X', 'O', 'O', 'D']
            ]
    graph = Graph(maze)
    solution = graph.solution
    print(f'The maze can be solved in {len(solution) - 1} steps.')
    graph.print_solution()
    print(f'Solution: {solution}\n')
