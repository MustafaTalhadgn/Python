from PyQt5.QtWidgets import QWidget, QPushButton, QInputDialog, QMessageBox
import sqlite3 as sql

class OperationsScreen(QWidget):
    def __init__(self, current_user):  # current_user parametresini bekleyen __init__ metodu
        super().__init__()
        self.setWindowTitle('Operations')
        self.setGeometry(100, 100, 300, 200)

        self.current_user = current_user  # current_user parametresini sınıfın özniteliğine atama

        change_password_button = QPushButton('şifreyi değiştir', self)
        change_password_button.clicked.connect(self.change_password)
        change_password_button.move(50, 30)

    def change_password(self):
        new_password, ok = QInputDialog.getText(self, 'şifre değiştir', 'şifreyi girin:')
        if ok:
            # SQLite veritabanına bağlanma ve şifreyi güncelleme işlemi
            connection = sql.connect('users.db')
            cursor = connection.cursor()
            cursor.execute('UPDATE users SET password=? WHERE username=?', (new_password, self.current_user))
            connection.commit()
            connection.close()
            QMessageBox.information(self, 'Success', 'şifre başarılı bir şekilde değişti ')