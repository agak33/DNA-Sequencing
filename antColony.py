import random

from graph import Graph
import constant as const
import numpy as np
from time import time


class AntColony(Graph):
    def __init__(self, file_path: str, max_len: int) -> None:
        super().__init__(file_path)
        self._best_path: list[int] = []
        self._best_solution: str = ''

        self._max_length = max_len
        self._pheromones = np.ones(shape=(len(self.node_labels), len(self.node_labels)))

        self.__probability_sums: list[float] = []
        self.__probabilities: np.ndarray = np.zeros(shape=(len(self.node_labels), len(self.node_labels)))

    def __convert_to_str(self, nodes: list[int]) -> str:
        """Converts node list to string"""
        solution: str = self.node_labels[nodes[0]]
        for i in range(1, len(nodes)):
            solution += self.node_labels[nodes[i]][
                        len(self.node_labels[nodes[i]]) - int(self.graph[nodes[i - 1], nodes[i]]):]
        return solution

    def __get_random_start_node(self) -> int:
        """Draws and returns random start node for ant"""
        return random.randrange(0, len(self.node_labels))

    def __get_list_max_probability(self, curr_node: int, available_nodes: list[int]) -> list[int]:
        """Finds max probability of choosing edge curr_node -> available_node,
        returns all available nodes with this value"""
        nodes: list[int] = []
        max_prob: float = 0

        for next_node in available_nodes:
            if self.__probabilities[curr_node, next_node] > max_prob:
                max_prob = self.__probabilities[curr_node, next_node]
                nodes = [next_node]
            elif self.__probabilities[curr_node, next_node] == max_prob:
                nodes.append(next_node)
        return nodes

    def __get_next_node(self,
                        curr_node: int,
                        visited_nodes: np.ndarray) -> int | None:
        """Returns next node index, based on probability"""
        available_nodes: list[int] = [
            index for index in range(len(self.graph[curr_node]))
            if self.graph[curr_node, index] > 0 and not visited_nodes[index]
        ]
        if not available_nodes:
            return None
        return random.choice(self.__get_list_max_probability(curr_node, available_nodes))

    def __calculate_probabilities(self) -> None:
        """Calculates probability of choosing certain edge for all edges"""
        self.__probability_sums = [
            sum(
                [
                    self._pheromones[node_index, z] ** const.ALPHA
                    * (self.word_len - self.graph[node_index, z]) ** const.BETA
                    for z in range(len(self.graph[node_index])) if self.graph[node_index, z] > 0
                ]
            )
            for node_index in range(len(self.graph))
        ]
        for i in range(len(self.__probabilities)):
            for j in range(len(self.__probabilities[i])):
                self.__probabilities[i, j] = 0 if not self.__probability_sums[i] else \
                    (self._pheromones[i, j] ** const.ALPHA
                     * (self.word_len - self.graph[i, j]) ** const.BETA
                     ) / self.__probability_sums[i]

    def __update_pheromones(self, temp_pheromones: np.ndarray) -> None:
        """Updates pheromones"""
        for i in range(len(self._pheromones)):
            for j in range(len(self._pheromones[i])):
                self._pheromones[i, j] = (1 - const.EVAPORATION_RATE) * self._pheromones[i, j] \
                                         + temp_pheromones[i, j]

    def __fitness(self, v: list[int]) -> None:
        """Calculates fitness"""
        if len(v) > len(self._best_path):
            self._best_path = v
            self._best_solution = self.__convert_to_str(v)

    def __perform_generation(self) -> None:
        """Runs single algorithm iteration"""
        temp_pheromones: np.ndarray = np.zeros(shape=(len(self.node_labels), len(self.node_labels)))
        visited: np.ndarray = np.zeros(shape=(len(self.node_labels),))
        self.__calculate_probabilities()

        for ant in range(const.COLONY_SIZE):
            curr_node: int = self.__get_random_start_node()
            visited[curr_node] = 1
            solution: list[int] = [curr_node]
            curr_cost: int = len(self.node_labels[curr_node])

            while True:
                curr_node = self.__get_next_node(curr_node, visited)
                curr_cost += self.graph[solution[-1], curr_node]
                if curr_node is None or curr_cost > self._max_length:
                    break
                visited[curr_node] = 1
                temp_pheromones[solution[-1], curr_node] += 1
                solution.append(curr_node)

            self.__fitness(solution)
            visited.fill(0)
        self.__update_pheromones(temp_pheromones)

    def solve(self) -> [list[int], str, float]:
        """
        Solves problem using ant colony optimization.
        :return: best founded DNA sequence and performance time
        """
        start: float = time()
        for generation in range(const.GENERATIONS):
            self.__perform_generation()
        end: float = time()
        return self._best_path, \
               f'{len(self._best_path)} / {len(self.node_labels)}', \
               self._best_solution, \
               len(self._best_solution), \
               end - start
