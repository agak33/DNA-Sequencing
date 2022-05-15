from __future__ import annotations

import random

from graph import Graph
import constant as const
from random import randint
from typing import Any
import numpy as np
from ant import Ant
from time import time


class AntColony(Graph):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._best_path: list[int] = []
        self._best_solution: str = ''
        self._max_length = int(file_path.replace('-', '.').replace('+', '.').split('.')[1])
        self._pheromones = np.zeros(shape=(len(self.node_labels), len(self.node_labels)))

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

    def __get_next_node(self,
                        curr_node: int,
                        visited_nodes: np.ndarray) -> int | None | Any:
        """Returns next node index, based on probability"""
        available_nodes: list[int] = [
            index for index in range(len(self.graph[curr_node]))
            if 0 < self.graph[curr_node, index] < 8 and not visited_nodes[index]
        ]
        if not available_nodes:
            return None
        return available_nodes[
            np.argmax([
                self.__get_probability(curr_node, next_node) for next_node in available_nodes
            ])
        ]

    def __get_probability(self,
                          curr_node: int,
                          next_node: int) -> float:
        """
        Calculates probability of choosing edge curr_node -> next_node
        :param curr_node: current node index
        :param next_node: next node index
        """
        if not self.graph[curr_node, next_node]:
            return 0
        try:

            return (self._pheromones[curr_node, next_node] ** const.ALPHA
                    * self.graph[curr_node, next_node] ** const.BETA
                    ) / (sum(
                        [
                            self._pheromones[curr_node, z] ** const.ALPHA * self.graph[curr_node, z] ** const.BETA
                            for z in range(len(self.graph[curr_node])) if self.graph[curr_node, z] > 0
                        ]))
        except ZeroDivisionError:
            return 0

    def __update_pheromones(self, temp_pheromones: np.ndarray) -> None:
        """Updates pheromones"""
        for i in range(len(self._pheromones)):
            for j in range(len(self._pheromones[i])):
                self._pheromones[i, j] = (1 - const.EVAPORATION_RATE) * self._pheromones[i, j] \
                                         + temp_pheromones[i, j]

    def __fitness(self, v: list[int]) -> None:
        """Calculates fitness"""
        if len(v) > len(self._best_path):
            s: str = self.__convert_to_str(v)
            self._best_path = v
            self._best_solution = s

    def __perform_generation(self) -> None:
        """Runs single algorithm iteration"""
        temp_pheromones: np.ndarray = np.zeros(shape=(len(self.node_labels), len(self.node_labels)))
        visited: np.ndarray = np.zeros(shape=(len(self.node_labels),))
        for ant in range(const.COLONY_SIZE):
            curr_node: int = self.__get_random_start_node()
            visited[curr_node] = 1
            solution: list[int] = [curr_node]

            while True:
                curr_node = self.__get_next_node(curr_node, visited)
                if curr_node is None:
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
        gen = 1
        for generation in range(const.GENERATIONS):
            print("generation ", gen)
            gen += 1
            self.__perform_generation()
        end: float = time()
        return self._best_path, len(self._best_path), self._best_solution, len(self._best_solution), end - start, self.node_labels
