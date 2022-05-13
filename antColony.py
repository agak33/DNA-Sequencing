from graph import Graph
import constant as const
from random import randint
import numpy as np
from ant import Ant
from time import time


class AntColony(Graph):
    def __init__(self, file_path: str):
        super().__init__(file_path)
        self._best_path: list[int] = []
        self._pheromones = np.zeros(shape=(len(self.node_labels), len(self.node_labels)))

    def __convert_to_str(self) -> str:
        # TODO best path -> str
        return ''

    def __get_probability(self, curr_node: int, next_node: int) -> float:
        """
        Calculates probability of choosing edge curr_node -> next_node
        :param curr_node: current node index
        :param next_node: next node index
        """
        if not self.graph[curr_node, next_node]:
            return 0
        return (self._pheromones[curr_node, next_node] ** const.ALPHA
                * self.graph[curr_node, next_node] ** const.BETA
                ) / (sum(
                    [
                        self._pheromones[curr_node, z] ** const.ALPHA * self.graph[curr_node, z] ** const.BETA
                        for z in range(len(self.graph[curr_node])) if self.graph[curr_node] > 0
                    ]))

    def __init_ants(self) -> None:
        """Initializes ant colony"""
        # TODO

    def __update_pheromones(self) -> None:
        """Updates pheromones"""
        # TODO

    def __fitness(self, v: list[int]) -> None:
        """Calculates fitness"""
        # TODO jezeli string jest dluzszy niz aktualne rozwiazanie -> podmieniamy listy

    def __perform_generation(self) -> None:
        """Runs single algorithm iteration"""
        # TODO
        m: np.ndarray = np.zeros(shape=(len(self.node_labels), len(self.node_labels)))
        solution: list[int] = []
        for ant in range(const.COLONY_SIZE):
            pass
            # TODO losowanie punktu startowy
            # TODO przechodzenie po grafie -> dodawanie do listy wierzcholkow
            self.__fitness(solution)

    def solve(self) -> [str, float]:
        """
        Solves problem using ant colony optimization.
        :return: best founded DNA sequence and performance time
        """
        # TODO
        start: float = time()
        for generation in range(const.GENERATIONS):
            self.__perform_generation()
            self.__update_pheromones()
        end: float = time()

        return self.__convert_to_str(), end - start
