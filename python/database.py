import sqlite3
import os

# AYARLAR VE DOSYA YOLLARI
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_FILE_PATH = os.path.join(CURRENT_DIR, "..", "sql", "tables.sql")
DB_PATH = os.path.join(CURRENT_DIR, "..", "bank.db")

def get_db_connection():
    """Veritabanına bağlanır."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"HATA: Veritabanına bağlanılamadı: {e}")
        return None

def create_tables():
    """tables.sql dosyasını çalıştırır (Tabloları SIFIRLAR)."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            if os.path.exists(SQL_FILE_PATH):
                with open(SQL_FILE_PATH, "r", encoding="utf-8") as f:
                    sql_script = f.read()
                    cursor.executescript(sql_script)
                    print("Tablolar başarıyla oluşturuldu (Eski veriler temizlendi).")
            else:
                print(f"UYARI: '{SQL_FILE_PATH}' bulunamadı.")
            conn.commit()
        except sqlite3.Error as e:
            print(f"Tablo hatası: {e}")
        finally:
            conn.close()

def add_customer(name):
    """Veritabanına yeni müşteri ekler (Sadece İsim)."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # SQL yapısına uygun sorgu:
            sql = "INSERT INTO customers (name) VALUES (?)"
            cursor.execute(sql, (name,))
            conn.commit()
            print(f"Başarılı: '{name}' sisteme eklendi.")
        except sqlite3.Error as e:
            print(f"Ekleme hatası: {e}")
        finally:
            conn.close()