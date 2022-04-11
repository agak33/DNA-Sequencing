
from typing import List
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class Instance(object):

    def __init__(self, file_path: str) -> None:
        self.node_labels: List[str] = []

        try:
            with open(file_path, 'r') as input_file:
                self.node_labels = [label.strip() for label in input_file]
        except FileNotFoundError:
            print(f'{file_path} was not found.')

        self.graph = np.zeros(shape=(len(self.node_labels), len(self.node_labels)))

        for index, label in enumerate(self.node_labels):
            matching = [i for i in range(index + 1, len(self.node_labels))
                        if label[1:] == self.node_labels[i][:-1]]

            for i in matching:
                self.graph[index][i] = 1
                self.graph[i][index] = -1

    def show_graph(self) -> None:
        graph = nx.from_numpy_array(self.graph)
        nx.draw(graph, pos=nx.random_layout(graph),
                #labels={k: v for k, v in enumerate(self.node_labels)},
                arrows=True, arrowsize=2, arrowstyle='simple',
                node_color='red', node_shape='s', node_size=10,
                font_size=11)
        plt.show()
        plt.close()


