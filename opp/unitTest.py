import unittest
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QComboBox, QPushButton, QLabel
from main import AddWindow
import time

class TestAddWindow(unittest.TestCase):
    start_time = time.time()
    def setUp(self):
        self.app = QApplication([])
        self.window = AddWindow()
        self.window.setFixedSize(300, 500)
        self.window.show()

    def tearDown(self):
        self.window.close()
        self.app.quit()

    def test_init(self):
        self.assertIsInstance(self.window, QMainWindow)
        self.assertIsInstance(self.window.name_label, QLabel)
        self.assertIsInstance(self.window.name_input, QComboBox)
        self.assertIsInstance(self.window.save_button, QPushButton)
        
    end_time = time.time()
    print("Время выполнения тестов:", end_time - start_time)
if __name__ == '__main__':
    unittest.main(verbosity=3)
