from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QMessageBox
import sqlite3 as sql
from menu_screen import MenuScreen

class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Kullanıcı Kayıt Sistemi')
        self.setGeometry(100, 100, 800, 600)

        self.username_label = QLabel('Kullanıcı Adı:', self)
        self.username_label.move(300, 150)
        self.username_input = QLineEdit(self)
        self.username_input.move(400, 150)

        self.password_label = QLabel('Şifreniz:', self)
        self.password_label.move(300, 190)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.move(400, 190)

        self.login_button = QPushButton('Giriş Yap', self)
        self.login_button.clicked.connect(self.login)
        self.login_button.move(300, 240)

        self.register_button = QPushButton('Kayıt Ol', self)
        self.register_button.clicked.connect(self.register)
        self.register_button.move(400, 240)

        # Veritabanı bağlantısını oluşturma
        self.connection = sql.connect('users.db')
        self.cursor = self.connection.cursor()

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Kullanıcıyı veritabanında arama
        self.cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = self.cursor.fetchone()

        if user:
            self.close()
            self.menu_screen = MenuScreen(username)  # current_user parametresini sağla
            self.menu_screen.show()
        else:
            QMessageBox.warning(self, 'Warning', 'Geçersiz kullanıcı adı veya şifre')

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Kullanıcıyı veritabanına ekleme
        try:
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            self.connection.commit()
            QMessageBox.information(self, 'Success', 'Kullanıcı Başarıyla Kayıt Edilmiştir')
        except sql.IntegrityError:
            QMessageBox.warning(self, 'Warning', 'Kulanıcı Adı Kullanılıyor')

    def closeEvent(self, event):
        self.connection.close()  # Uygulama kapatıldığında veritabanı bağlantısını kapat
