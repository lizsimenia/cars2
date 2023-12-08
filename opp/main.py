import typing
from PyQt6 import QtCore
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QComboBox

import pattern_ch

class Car:
    def __init__(self, name, manufacturer,
                 model_range, color, engine_type):
        self.num = name
        self.manufacturer = manufacturer
        self.model_range = model_range
        self.color = color
        self.engine_type = engine_type


class AddWindow(QMainWindow):
    def __init__(self, start = 0, end = len(pattern_ch.info_pattern)):
        super().__init__()
        self.setWindowTitle("Adding car")
        self.setFixedSize(QSize(300, 500))

        layout = QVBoxLayout()
        central_widget = QWidget()

        self.info = []
        self.input_fields = []

        for i_spec in list(pattern_ch.info_pattern)[start:end]:
            self.name_label = QLabel(f"{i_spec}*:")
            if isinstance(pattern_ch.info_pattern[i_spec], list):
                self.name_input = QComboBox()
                self.name_input.addItems(pattern_ch.info_pattern[i_spec])
            else:
                self.name_input = QLineEdit()
                if i_spec == "Номер машины":
                    self.name_input.textChanged.connect(self.validate_num)
                elif i_spec == "Цвет" or i_spec == "Производитель":
                    self.name_input.textChanged.connect(self.validate_text)
                else:
                     self.name_input.textChanged.connect(self.validate)
                self.name_input.returnPressed.connect(self.move_focus)

            layout.addWidget(self.name_label)
            layout.addWidget(self.name_input)

            self.info.append(self.name_input)
            self.input_fields.append(self.name_input)

            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)

        self.save_button = QPushButton("Сохранить")
        self.save_button.setEnabled(False)

        if start == 0:
            self.save_button.clicked.connect(self.save_info)
        layout.addWidget(self.save_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        for input_field in self.input_fields:
            if isinstance(input_field, QLineEdit):
                input_field.textChanged.connect(self.validate_data)

        if all(i for i in self.input_fields if isinstance(i, QComboBox)):
            self.save_button.setEnabled(True)

    def validate_data(self):
        temp = []
        for input_field in self.input_fields:
            if isinstance(input_field, QLineEdit):
                temp.append(input_field.styleSheet() == "QLineEdit { background-color: white; }")
        self.save_button.setEnabled(all(i == 1 for i in temp))
        print(temp)

    # перемещает фокус на след строку
    def move_focus(self):
        current_index = -1
        for index, input_field in enumerate(self.input_fields):
            if input_field.hasFocus():
                current_index = index
                break
        next_index = (current_index + 1) % len(self.input_fields)
        self.input_fields[next_index].setFocus()

    # проверки
    def validate(self, text):
        input_field = self.sender()
        if text == "":
            input_field.setStyleSheet("QLineEdit { background-color: rgb(255, 200, 200); }")
            return 1
        else:
            input_field.setStyleSheet("QLineEdit { background-color: white; }")

    def validate_num(self, text):
        input_field = self.sender()
        try:
            if len(text) >= 8\
                and text[0] in 'АВЕКМНОРСТУХ' and (0 <= int(text[1:4]) < 1000)\
                and text[4] in 'АВЕКМНОРСТУХ'\
                and text[5] in 'АВЕКМНОРСТУХ'and (0 <= int(text[-2:]) < 1000):
             input_field.setStyleSheet("QLineEdit { background-color: white; }")
             return 1
            else:
                raise Exception
        except Exception:
            input_field.setStyleSheet("QLineEdit { background-color: rgb(255, 200, 200); }")

    def validate_text(self, text):
        input_field = self.sender()
        if text.isalpha():
            input_field.setStyleSheet("QLineEdit { background-color: white; }")
            return 1
        else:
             input_field.setStyleSheet("QLineEdit { background-color: rgb(255, 200, 200); }")

    def save_info(self):
        saved_info = []
        for input_field in self.info:
            text = input_field.currentText() if isinstance(input_field, QComboBox) else input_field.text()
            saved_info.append(text)

        with open("cars.txt", "a", encoding = "UTF-8") as file:
            file.write("\n".join(saved_info) + "\nend\n")

        print(saved_info)
        self.close()

class RemovalWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Remove car")

        self.setFixedSize(QSize(200, 200))

        layout = QVBoxLayout()
        central_widget = QWidget()
        self.error_label= QLabel("")
        self.error_label.setStyleSheet("color: pink")

        self.name_label = QLabel("Номер машины*:")
        self.name_input = QLineEdit()
        self.delete_button = QPushButton("Удалить")

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.error_label)
        layout.addWidget(self.delete_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.name_input.textChanged.connect(self.validate_numm)
        self.delete_button.clicked.connect(self.remove)


    def validate_numm(self, text):
        input_field=self.sender()
        try:
            if len(text)>=8\
                and text[0] in 'АВЕКМНОРСТУХ' and (0 <= int(text[1:4])<1000) \
                and text[4] in 'АВЕКМНОРСТУХ'\
                and text[5] in 'АВЕКМНОРСТУХ' and (0 <= int(text[-2:])<1000):
                input_field.setStyleSheet("QLineEdit{background-color:white;}")
                self.error_label.setText("")
            else:
                raise Exception
        except Exception:
            self.error_label.setText("Неверно введен номер")

    def remove(self, text):
        index = None
        with open("cars.txt", "r", encoding = "UTF-8") as file:
            lines = file.readlines()
            for i, value in enumerate(lines):
                if value[:-1] == self.name_input.text():
                    index = i
                    break
            if index != None:
                del lines[index:index+len(pattern_ch.info_pattern)+1]
                print(lines)
                with open('cars.txt', 'w', encoding='UTF8') as file:
                    file.writelines(lines)
            else:
                print("POPOP")
        self.close()

class SearchWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Searching Car")
        self.setFixedSize(QSize(500, 500))

        layout = QVBoxLayout()
        central_widget = QWidget()

        self.name_label = QLabel("Поиск по:")
        self.name_input = QLineEdit()
        self.search_button = QPushButton("Найти")

        self.table = QTableWidget(self)
        self.table.setColumnCount(len(pattern_ch.info_pattern))
        self.table.setRowCount(100)

        self.table.setHorizontalHeaderLabels([name for name in pattern_ch.info_pattern])

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.table)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.search_button.clicked.connect(self.search)

    def search(self):
        self.table.clearContents()
        lines = []
        temp = []
        with open('cars.txt', 'r', encoding = 'UTF-8') as file:
            for i in file:
                if i[:-1] != 'end':
                    temp.append(i[:-1])
                else:
                    lines.append(temp)
                    temp = []

        row, column = 0, 0
        for i_line in lines:
            if self.name_input.text() in i_line:
                for value in i_line:
                    self.table.setItem(row, column, QTableWidgetItem(value))
                    column += 1
                print(i_line, row, column)
                row += 1
                column = 0

        self.table.resizeColumnsToContents()


class DisplayWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Display Car")
        self.setFixedSize(QSize(500, 500))

        layout = QVBoxLayout()
        central_widget = QWidget()

        self.ok_button = QPushButton("ОК")

        self.table = QTableWidget(self)
        self.table.setColumnCount(len(pattern_ch.info_pattern))
        self.table.setRowCount(100)

        self.table.setHorizontalHeaderLabels([name for name in pattern_ch.info_pattern])

        layout.addWidget(self.ok_button)
        layout.addWidget(self.table)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.ok_button.clicked.connect(self.back)

        lines = []
        temp = []
        with open('cars.txt', 'r', encoding = 'UTF-8') as file:
            for i in file:
                if i[:-1] != 'end':
                    temp.append(i[:-1])
                else:
                    lines.append(temp)
                    temp = []
        print(lines)
        row, column = 0, 0
        for i_line in lines:
            for value in i_line:
                self.table.setItem(row, column, QTableWidgetItem(value))
                column += 1
            print(i_line, row, column)
            row += 1
            column = 0

        self.table.resizeColumnsToContents()

    def back(self):
        self.close()

class EditWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit car")
        self.setFixedSize(QSize(300, 200))

        self.layout = QVBoxLayout()
        self.central_widget = QWidget()

        self.name_label = QLabel("Номер машины:")
        self.name_input = QLineEdit()
        self.ask_label = QLabel("Характеристика для изменения:")
        self.ask_input = QComboBox()
        self.ask_input.addItems([i for i in pattern_ch.info_pattern][3:])

        self.edit_button = QPushButton("Изменить")

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.ask_label)
        self.layout.addWidget(self.ask_input)
        self.layout.addWidget(self.edit_button)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.edit_button.clicked.connect(self.edit)

    def edit(self):
        index = None
        with open("cars.txt", "r", encoding = "UTF-8") as file:
            self.lines = file.readlines()
            for i, value in enumerate(self.lines):
                if value[:-1] == self.name_input.text():
                    index = i
                    break
            if index != None:
                keys = [i for i in pattern_ch.info_pattern]
                index_find = keys.index(self.ask_input.currentText())

                self.window = AddWindow(index_find, index_find+1)
                self.window.setFixedSize(100, 100)
                self.window.setWindowTitle("Edit...")

                self.window.show()
                self.index = index_find + index
                self.window.save_button.clicked.connect(self.rewrite_line)

    def rewrite_line(self):
        self.new_data = self.window.name_input.currentText() if isinstance(self.window.name_input, QComboBox)\
                    else self.window.name_input.text()
        with open("cars.txt", "w", encoding = "UTF-8") as file:
            self.lines[self.index] = self.new_data + '\n'
            print(self.lines[self.index])
            file.writelines(self.lines)
        self.window.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Car Accounting")

        self.setFixedSize(QSize(300, 200))

        self.add_button = QPushButton("Добавить")
        self.delete_button = QPushButton("Удалить")
        self.edit_button =  QPushButton("Изменить")
        self.search_button = QPushButton("Найти")
        self.display_button = QPushButton("Список машин")
        self.exit_button = QPushButton("Выход")
        

        layout = QVBoxLayout()
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.search_button)
        layout.addWidget(self.display_button)
        layout.addWidget(self.exit_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.add_button.clicked.connect(self.adding)
        self.delete_button.clicked.connect(self.removal)
        self.search_button.clicked.connect(self.search)
        self.display_button.clicked.connect(self.display)
        self.edit_button.clicked.connect(self.edit)

    def exit(self):
        self.close()
        
    def display(self):
        self.display_window = DisplayWindow()
        self.display_window.show()

    def adding(self):
        self.adding_window = AddWindow()
        self.adding_window.show()

    def removal(self):
        self.removal_window = RemovalWindow()
        self.removal_window.show()

    def search(self):
        self.search_window = SearchWindow()
        self.search_window.show()

    def edit(self):
        self.edit_window = EditWindow()
        self.edit_window.show()


# Create the application instance and main window
app = QApplication([])
window = MainWindow()
window.show()
app.exec()
