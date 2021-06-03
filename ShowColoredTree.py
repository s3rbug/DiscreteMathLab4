import sys
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import networkx as nx
from Logic import Logic
from PyQt5 import QtCore


class ShowColoredTree(QDialog):
    def __init__(self, logic: Logic, ):
        super(ShowColoredTree, self).__init__()
        self.logic = logic
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint
        )
        self.setWindowTitle("Розфарбований граф")
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas, stretch=1)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.plot()

    def plot(self):
        self.figure.clear()
        graph = self.logic.nx_graph
        colors = ['red', 'purple', 'green', 'yellow', 'blue']
        coloring = nx.algorithms.coloring.greedy_color(self.logic.nx_graph)
        node_colors = [colors[coloring[e]] for e in graph.nodes]
        pos = nx.spring_layout(graph)
        nx.draw_networkx_nodes(graph, pos, node_size=500, node_color=node_colors)
        nx.draw_networkx_labels(graph, pos)
        nx.draw_networkx_edges(graph, pos, arrows=True)
        plt.axis('off')
        self.canvas.draw()
