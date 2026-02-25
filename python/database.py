import sqlite3
import os

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
    """tables.sql dosyasını çalıştırır. (SIFIRLAR)"""
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
    """Veritabanına yeni müşteri ekler (İsim)."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO customers (name) VALUES (?)"
            cursor.execute(sql, (name,))
            conn.commit()
            print(f"Başarılı: '{name}' sisteme eklendi.")
        except sqlite3.Error as e:
            print(f"Ekleme hatası: {e}")
        finally:
            conn.close()

def get_customers():
    """Hesap açarken listeden seçmek için müşterileri sıralar."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customers")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Listeleme hatası: {e}")
        finally:
            conn.close()
    return []

def create_account(customer_id):
    """Seçilen müşterinin ID'sine göre 0 bakiye ile yeni bir hesap açar."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # yeni eklenen MÜŞTERİ kontrolü
            cursor.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,))
            musteri = cursor.fetchone()
            
            if not musteri:
                print("HATA: Böyle bir müşteri bulunamadı! Lütfen listedeki geçerli bir Müşteri ID girin.")
                return 
            

            cursor.execute("INSERT INTO accounts (customer_id, balance) VALUES (?, 0)", (customer_id,))
            conn.commit()
            print(f"Başarılı: '{musteri['name']}' (ID: {customer_id}) için yeni hesap oluşturuldu.")
        except sqlite3.Error as e:
            print(f"Hesap oluşturma hatası: {e}")
        finally:
            conn.close()

def get_accounts():
    """Hesapları, müşteri isimleriyle eşleştirerek (JOIN) getirir."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                SELECT 
                    customers.customer_id,
                    customers.name AS musteri_adi,
                    accounts.account_id AS hesap_no,
                    accounts.balance AS bakiye
                FROM accounts
                JOIN customers ON accounts.customer_id = customers.customer_id
                ORDER BY customers.name;
            """
            cursor.execute(query)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Hesap listeleme hatası: {e}")
        finally:
            conn.close()
    return []

def deposit(account_id, amount):
    """Belirtilen hesaba para yatırır (Deposit). ledger/transaction kaydı atar."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # yeni eklenen HESAP kontrolü
            cursor.execute("SELECT * FROM accounts WHERE account_id = ?", (account_id,))
            hesap = cursor.fetchone()
            
            if not hesap:
                print("HATA: Böyle bir hesap bulunamadı! Lütfen geçerli bir Hesap No girin.")
                return 
            
            # işlem tablosuna kayıt
            cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, 'deposit', ?)", (account_id, amount))
            transaction_id = cursor.lastrowid
            
            # hesap bakiye güncelleme
            cursor.execute("UPDATE accounts SET balance = balance + ? WHERE account_id = ?", (amount, account_id))
            
            # Ledger kaydı
            cursor.execute("INSERT INTO ledger (transactions_id, debit_account, credit_account, amount) VALUES (?, ?, 0, ?)", (transaction_id, account_id, amount))
            
            conn.commit()
            print(f"Başarılı: {account_id} numaralı hesaba {amount} TL yatırıldı.")
        except sqlite3.Error as e:
            conn.rollback()
            print(f"HATA: Para yatırma işlemi başarısız: {e}")
        finally:
            conn.close()

def withdraw(account_id, amount):
    """Belirtilen hesaptan para çeker (Withdraw) ve bakiye kontrolü yapar."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Veritabanında ID arama
            cursor.execute("SELECT balance FROM accounts WHERE account_id = ?", (account_id,))
            hesap = cursor.fetchone()
            
            # Hesap hiç yoksa diye
            if hesap is None:
                print(f"HATA: {account_id} numaralı bir hesap bulunamadı! Lütfen geçerli bir Hesap No girin.")
                return # İşlemi burada durdur
            
            # Hesap var ama içindeki para çekilmek istenenden azsa
            if hesap['balance'] < amount:
                print(f"HATA: Yetersiz bakiye! Mevcut bakiye: {hesap['balance']} TL")
                return 

            # işlem (Transaction) tablosuna kayıt
            cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, 'withdraw', ?)", (account_id, amount))
            transaction_id = cursor.lastrowid
            
            # Hesabın bakiyesini düşürme
            cursor.execute("UPDATE accounts SET balance = balance - ? WHERE account_id = ?", (amount, account_id))
            
            # Ledger kaydı atma (F'nin mantığı: debit 0, credit hesap)
            cursor.execute("INSERT INTO ledger (transactions_id, debit_account, credit_account, amount) VALUES (?, 0, ?, ?)", (transaction_id, account_id, amount))
            
            conn.commit()
            print(f"Başarılı: {account_id} numaralı hesaptan {amount} TL çekildi.")
        except sqlite3.Error as e:
            conn.rollback() # Bir hata çıkarsa işlemleri geri alma
            print(f"HATA: Para çekme işlemi başarısız: {e}")
        finally:
            conn.close()