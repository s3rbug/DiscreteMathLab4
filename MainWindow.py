import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic
from utils import show_message, can_convert_str_to_int, center_item
from PyQt5.QtGui import QFont, QFontDatabase
from Logic import Logic
from ShowColoredTree import ShowColoredTree


def print_variant():
    number = 102  # Номер заліковки
    variant = number % 6 + 1
    output = "Ім'я: Бугайчук Сергій Володимирович" + \
             "\nГрупа: ІО-01" + \
             "\nНомер у групі: 2"
    output += "\nВаріант: " + str(variant)
    show_message(output, QMessageBox.Information, "Інформація про студента")


class MainWindow(QMainWindow):
    def update_table(self):
        n = len(self.logic.graph)
        self.table.setRowCount(n)
        self.table.setColumnCount(n)
        self.table.setVerticalHeaderLabels([str(i) for i in range(n)])
        self.table.setHorizontalHeaderLabels([str(i) for i in range(n)])
        for i in range(n):
            for j in range(n):
                self.table.setItem(i, j, center_item(self.logic.graph[i][j]))
        self.showTree.plot()

    def save_info(self):
        node = self.enter_count_node.text()
        edge = self.enter_count_edge.text()
        if not can_convert_str_to_int(node):
            show_message("Неправильно введена кількість вершин")
            return
        if not can_convert_str_to_int(edge):
            show_message("Неправильно введена кількість ребер")
            return
        node, edge = int(node), int(edge)
        if edge > node * (node - 1) // 2:
            show_message("Неправильно введена кількість ребер та вершин")
            return
        if node < 1:
            show_message("Кількість вершин повинна бути більша одиниці")
            return
        if edge < node - 1:
            show_message("Кількість ребер повинна бути більша або рівна кількості вершин мінус один")
            return
        self.logic.save_info(node, edge)
        self.logic.generate_empty_graph()
        self.update_table()

    def set_custom_graph(self):
        self.logic.generate_custom_graph()
        self.set_nodes_edges_info()
        self.update_table()

    def set_nodes_edges_info(self):
        self.enter_count_node.setText(str(self.logic.count_node))
        self.enter_count_edge.setText(str(self.logic.count_edge))

    def generate_random(self):
        self.logic.generate_random_graph()
        self.update_table()

    def change_item(self, item):
        i, j = item.row(), item.column()
        if item.text() != str(self.logic.graph[i][j]):
            if not can_convert_str_to_int(item.text()):
                show_message("Неправильно уведені дані")
                self.update_table()
            else:
                self.logic.graph[i][j] = self.logic.nx_graph[i][j]['weight'] = int(item.text())
                self.showTree.plot()

    @staticmethod
    def show_window(value):
        if isinstance(value, list):
            def foo():
                for i in value:
                    i.show()
            return foo
        return lambda: value.show()

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('MainWindowForm.ui', self)
        self.logic = Logic()
        self.showTree = ShowColoredTree(self.logic)
        self.info.triggered.connect(print_variant)
        self.generate_random_button.clicked.connect(self.generate_random)
        self.save.clicked.connect(self.save_info)
        self.table.itemChanged.connect(self.change_item)
        self.show_tree.clicked.connect(self.show_window([self.showTree]))
        self.set_graph.clicked.connect(self.set_custom_graph)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    font_database = QFontDatabase()
    font_database.addApplicationFont("./assets/Lucida Grande.ttf")
    font = QFont("Lucida Grande")
    QApplication.setFont(font)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
