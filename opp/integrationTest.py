import unittest
from PyQt6.QtWidgets import QApplication
from main import AddWindow, RemovalWindow, SearchWindow, DisplayWindow, EditWindow

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])

    def tearDown(self):
        self.app.quit()

    def test_add_remove_car(self):
        add_window = AddWindow()
        add_window.info[0].setText("А100АА88")
        add_window.info[1].setText("BMW")
        add_window.info[2].setText("RTX1000")
        add_window.info[3].setText("Синий")
        add_window.info[4].setCurrentIndex(1)
        add_window.save_info()

        search_window = SearchWindow()
        search_window.name_input.setText("А100АА88")
        search_window.search()
        self.assertEqual(search_window.table.item(0,0).text(), "А100АА88")

        remove_window = RemovalWindow()
        remove_window.name_input.setText("А100АА88")
        remove_window.remove("А100АА88")

        search_window = SearchWindow()
        search_window.name_input.setText("А100АА88")
        search_window.search()
        self.assertEqual(search_window.table.item(0,0), None)

    # def test_edit_car(self):
    #     add_window = AddWindow()
    #     add_window.info[0].setText("А100АА88")
    #     add_window.info[1].setText("BMW")
    #     add_window.info[2].setText("RTX1000")
    #     add_window.info[3].setText("Синий")
    #     add_window.info[4].setCurrentIndex(1)
    #     add_window.save_info()

    #     edit_window = EditWindow()
    #     edit_window.name_input.setText("А100АА88")
    #     edit_window.ask_input.setCurrentIndex(0)
    #     edit_window.edit_button.click()
    #     add_window.info[3].setText("Красный")

    #     search_window = SearchWindow()
    #     search_window.name_input.setText("А100АА88")
    #     search_window.search()
    #     self.assertEqual(search_window.table.item(0, 3).text(), "Красный")

if __name__ == '__main__':
    unittest.main(verbosity=3)
