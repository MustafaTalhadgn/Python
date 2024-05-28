from PyQt5.QtWidgets import QWidget, QPushButton, QTextEdit, QMessageBox
import sqlite3 as sql

class CompareScreen(QWidget):
    def __init__(self,current_user):
        super().__init__()
        self.setWindowTitle('Metin Karşılaştırma')
        self.setGeometry(100, 100, 800, 600)

        self.textbox1 = QTextEdit(self)
        self.textbox1.setGeometry(150, 100, 300, 100)

        self.textbox2 = QTextEdit(self)
        self.textbox2.setGeometry(150, 220, 300, 100)

        compare_button = QPushButton('Karşılaştır', self)
        compare_button.clicked.connect(self.compare_texts)
        compare_button.setGeometry(150, 340, 100, 30)

    def compare_texts(self):
        text1 = self.textbox1.toPlainText()
        text2 = self.textbox2.toPlainText()

        # SQLite veritabanına metinleri ekleme
        add_texts_to_database(text1, text2)

        # Jaccard benzerlik katsayısı hesapla
        similarity_score_jaccard = jaccard_similarity(text1, text2)

        # Levenshtein uzaklık hesapla
        distance_score_levenshtein = levenshtein_distance(text1, text2)

        # Sonuçları ekrana yazdır
        result_message = f"Jaccard Similarity: {similarity_score_jaccard:.2f}\nLevenshtein Distance: {distance_score_levenshtein}"
        QMessageBox.information(self, 'Comparison Result', result_message)


def add_texts_to_database(text1, text2):
    # SQLite veritabanına bağlanma
    connection = sql.connect('sqlite.db')
    cursor = connection.cursor()

    # Metinleri veritabanına ekleme
    cursor.execute('INSERT INTO metinler (metin) VALUES (?)', (text1,))
    cursor.execute('INSERT INTO metinler (metin) VALUES (?)', (text2,))

    # Değişiklikleri kaydetme ve bağlantıyı kapatma
    connection.commit()
    connection.close()


def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def jaccard_similarity(metin1, metin2):
    # Metinleri kelimelere ayırma ve kümelerini oluşturma
    set1 = set(metin1.split())
    set2 = set(metin2.split())
    
    # Kesişim ve birleşim kümelerini bulma
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    # Jaccard benzerlik katsayısını hesaplama
    similarity = intersection / union
    return similarity
