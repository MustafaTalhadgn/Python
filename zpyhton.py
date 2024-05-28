import sqlite3 as sql

def create_database():
    # SQLite veritabanı bağlantısı oluşturma
    baglan = sql.connect('sqlite.db')
    imlec = baglan.cursor()

    # Metinler tablosunu oluşturma
    imlec.execute("CREATE TABLE IF NOT EXISTS metinler(metin TEXT)")

    # Metinleri veritabanına ekleme
    metin1 = "insan olmak değişik"
    metin2 = "insan olmak için"
    imlec.execute('INSERT INTO metinler (metin) VALUES(?)', (metin1,))
    imlec.execute('INSERT INTO metinler (metin) VALUES(?)', (metin2,))

    # Değişiklikleri kaydetme ve bağlantıyı kapatma
    baglan.commit()
    baglan.close()
    

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


def databaseDelete():
    # Veritabanındaki verileri silme
    imlec.execute('DELETE FROM metinler')
    baglan.commit()
    baglan.close()


# SQLite veritabanına metinleri ekleyelim
create_database()

# SQLite veritabanından metinleri çekelim
baglan = sql.connect('sqlite.db')
imlec = baglan.cursor()
imlec.execute('SELECT metin FROM metinler')
texts = [satir[0] for satir in imlec.fetchall()]

# Benzerlik testini gerçekleştirelim
similarity_score = jaccard_similarity(texts[0], texts[1])
print(f"Jaccard Similarity: {similarity_score:.2f}")

# Benzerlik durumunu bir dosyaya yazalım
with open('benzerlik_durumu.txt', 'w') as file:
    file.write(f"Jaccard Similarity: {similarity_score:.2f}")
    databaseDelete()

