# menu_screen.py
from PyQt5.QtWidgets import QWidget, QPushButton
from operations_screen import OperationsScreen
from compare_screen import CompareScreen

class MenuScreen(QWidget):
    def __init__(self, current_user):  
        super().__init__()
        self.setWindowTitle('Menu')
        self.setGeometry(100, 100, 800, 600)
        self.current_user = current_user

        compare_button = QPushButton('Metin Karşılaştır', self)
        compare_button.clicked.connect(self.compare_menu)
        compare_button.move(300, 230)

        operations_button = QPushButton('İşlemler', self)
        operations_button.clicked.connect(self.operations_menu)
        operations_button.move(300, 270)

        exit_button = QPushButton('Çıkış', self)
        exit_button.clicked.connect(self.close)
        exit_button.move(300, 310)

    def operations_menu(self):
        self.operations_screen = OperationsScreen(self.current_user)  # current_user parametresini ileterek OperationsScreen örneği oluştur
        self.operations_screen.show()

    def compare_menu(self):
        self.compare_screen = CompareScreen(self.current_user)  # current_user parametresini ileterek CompareScreen örneği oluştur
        self.compare_screen.show()
