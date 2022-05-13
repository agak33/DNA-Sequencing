import numpy as np


class Graph:

    def __init__(self, file_path: str) -> None:
        """
        Creates an object to represent instance problem
        :param file_path: path to the file with all words from spectrum
        """
        self.word_len: int = 0
        try:
            with open(file_path, 'r') as input_file:
                self.node_labels = [label.strip() for label in input_file]
                self.word_len: int = len(self.node_labels[0])
        except FileNotFoundError:
            print(f'{file_path} was not found.')
            self.node_labels = []
        except IndexError:
            pass

        self.graph = np.zeros(shape=(len(self.node_labels), len(self.node_labels)))
        self.__build_graph()

    def __build_graph(self) -> None:
        """
        Creates a directed graph (represents by the matrix), based on labels given in input.
        """
        for node_index in range(len(self.node_labels)):
            for target_index in range(len(self.node_labels)):
                self.graph[node_index][target_index] = self.__get_cost_between(
                    self.node_labels[node_index], self.node_labels[target_index]
                ) if node_index != target_index else 0
        print(self.graph)

    @staticmethod
    def __get_cost_between(node_1: str, node_2: str) -> int:
        """
        Calculates cost between two nodes, based on their labels.
        """
        for i in range(1, len(node_1)):
            if node_1[i:] == node_2[:-i]:
                return i
        return 0
