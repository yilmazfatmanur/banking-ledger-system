import sqlite3
import os
from decimal import Decimal

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
    """Para yatırma işlemi."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Hesap kontrolü
            cursor.execute("SELECT * FROM accounts WHERE account_id = ?", (account_id,))
            if not cursor.fetchone():
                print("HATA: Hesap bulunamadı!")
                return

            final_amount_float = float(amount) 

            # İşlem Kaydı 
            cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, 'deposit', ?)", (account_id, final_amount_float))
            t_id = cursor.lastrowid
            
            # Bakiye Güncelleme 
            cursor.execute("UPDATE accounts SET balance = balance + ? WHERE account_id = ?", (final_amount_float, account_id))
            
            # Ledger Kaydı
            cursor.execute("INSERT INTO ledger (transactions_id, debit_account, credit_account, amount) VALUES (?, ?, 0, ?)", (t_id, account_id, final_amount_float))
            
            conn.commit()
            print(f"Başarılı: {account_id} nolu hesaba {amount} TL yatırıldı.")
        except sqlite3.Error as e:
            conn.rollback()
            print(f"İşlem Hatası: {e}")
        finally:
            conn.close()

def withdraw(account_id, amount):
    """Para çekme işlemi."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Bakiye Kontrolü (Veritabanından gelen veriyi Decimal yapıp kıyaslama)
            cursor.execute("SELECT balance FROM accounts WHERE account_id = ?", (account_id,))
            hesap = cursor.fetchone()
            
            if not hesap:
                print("HATA: Hesap bulunamadı!")
                return
            
            # Veritabanındaki bakiyeyi Decimal'a çevirip kontrol etmece
            mevcut_bakiye = Decimal(str(hesap['balance']))
            
            if mevcut_bakiye < amount:
                print(f"HATA: Yetersiz bakiye! (Mevcut: {mevcut_bakiye} TL)")
                return

            final_amount_float = float(amount)

            #İşlem Kaydı
            cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, 'withdraw', ?)", (account_id, final_amount_float))
            t_id = cursor.lastrowid
            
            # Bakiye Düşme
            cursor.execute("UPDATE accounts SET balance = balance - ? WHERE account_id = ?", (final_amount_float, account_id))
            
            # Ledger Kaydı
            cursor.execute("INSERT INTO ledger (transactions_id, debit_account, credit_account, amount) VALUES (?, 0, ?, ?)", (t_id, account_id, final_amount_float))
            
            conn.commit()
            print(f"Başarılı: {account_id} nolu hesaptan {amount} TL çekildi.")
        except sqlite3.Error as e:
            conn.rollback()
            print(f"İşlem Hatası: {e}")
        finally:
            conn.close()

def run_sql_file(filename):
    "Belirtilen sql dosyasını çalıştırır."
    conn = get_db_connection()
    if conn:
        try:
            file_path = os.path.join(CURRENT_DIR, "..", "sql", filename)
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    sql_script = f.read()
                    cursor = conn.cursor()
                    cursor.executescript(sql_script)
                    conn.commit()
                    print(f"'{filename}' başarıyla çalıştırıldı.")
            else:
                print(f"HATA: '{filename}' bulunamadı.")
        except sqlite3.Error as e:
           conn.rollback()
           print(f"HATA: SQL hatası: {e}")
        finally:
            conn.close()

def insert_test_data():
    """Test verisi ekler(insert_database.sql dosyasını çalıştırır)."""
    print("\n--- Test verisi ekleniyor...")
    run_sql_file("insert_database.sql")

def transfer(gonderen_id, alici_id, miktar):
    """İki hesap arası para transferi."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # gönderen Bakiye Kontrolü
            cursor.execute("SELECT balance FROM accounts WHERE account_id = ?", (gonderen_id,))
            gonderen = cursor.fetchone()
            
            # alıcı Hesap Kontrolü
            cursor.execute("SELECT account_id FROM accounts WHERE account_id = ?", (alici_id,))
            alici = cursor.fetchone()
            
            if not gonderen:
                print("HATA: Gönderen hesap bulunamadı.")
                return
            if not alici:
                print("HATA: Alıcı hesap bulunamadı.")
                return
            
            # Decimal ile Bakiye Kontrolü
            mevcut_bakiye = Decimal(str(gonderen['balance']))
            if mevcut_bakiye < miktar:
                print("HATA: Yetersiz bakiye!")
                return

            
            final_amount_float = float(miktar)

            # gönderen Hesaptan Çıkış
            cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, 'transfer_out', ?)", (gonderen_id, final_amount_float))
            
            # alıcı Hesaba Giriş
            cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, 'transfer_in', ?)", (alici_id, final_amount_float))
            t_id = cursor.lastrowid 

            # update 
            cursor.execute("UPDATE accounts SET balance = balance - ? WHERE account_id = ?", (final_amount_float, gonderen_id))
            cursor.execute("UPDATE accounts SET balance = balance + ? WHERE account_id = ?", (final_amount_float, alici_id))
            
            #ledger Kaydı
            cursor.execute("INSERT INTO ledger (transactions_id, debit_account, credit_account, amount) VALUES (?, ?, ?, ?)", (t_id, alici_id, gonderen_id, final_amount_float))
            
            conn.commit()
            print(f"Transfer Başarılı: {gonderen_id} -> {alici_id} ({miktar} TL)")
            
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Transfer Hatası: {e}")
        finally:
            conn.close()

def get_transaction_history(account_id):
    """Belirli bir hesabın işlem geçmişini getirir."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                SELECT 
                    t.transactions_id,
                    t.type AS islem_tipi,
                    t.amount AS tutar,
                    a.balance AS guncel_bakiye
                FROM transactions t 
                JOIN accounts a ON t.account_id = a.account_id
                WHERE t.account_id = ?
                ORDER BY t.transactions_id DESC;
            """
            cursor.execute(query, (account_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"HATA: Rapor çekilemedi: {e}")
        finally:
            conn.close()
    return []

def get_bank_summary():
    """
    Bankanın genel durum özetini (Toplam Mevduat, Çekilen, Yatırılan) getirir.
    GÜNCELLEME: Toplam yatırılan ve çekilen paralar eklendi.
    """
    conn = get_db_connection()
    summary = {}
    if conn:
        try:
            cursor = conn.cursor()
            
           
            cursor.execute("SELECT COUNT(*) as sayi FROM customers")
            summary['musteri_sayisi'] = cursor.fetchone()['sayi']
            
            cursor.execute("SELECT COUNT(*) as sayi FROM accounts")
            summary['hesap_sayisi'] = cursor.fetchone()['sayi']
            
            # Toplam Bakiye
            cursor.execute("SELECT SUM(balance) as toplam FROM accounts")
            res = cursor.fetchone()['toplam']
            summary['toplam_para'] = res if res else 0

            # Toplam Yatırılan (Deposit)
            cursor.execute("SELECT SUM(amount) as toplam FROM transactions WHERE type='deposit'")
            res_dep = cursor.fetchone()['toplam']
            summary['toplam_yatirilan'] = res_dep if res_dep else 0

            # Toplam Çekilen (Withdraw)
            cursor.execute("SELECT SUM(amount) as toplam FROM transactions WHERE type='withdraw'")
            res_with = cursor.fetchone()['toplam']
            summary['toplam_cekilen'] = res_with if res_with else 0
            
            return summary
        except sqlite3.Error as e:
            print(f"Özet hatası: {e}")
        finally:
            conn.close()
    return {}

def get_active_stats():
    """
    En aktif müşteri ve en çok para gönderen hesabı bulur.
    """
    conn = get_db_connection()
    stats = {}
    if conn:
        try:
            cursor = conn.cursor()
            
            # En Aktif Müşteri 
            query_active = """
                SELECT c.name, COUNT(t.transactions_id) as islem_sayisi
                FROM transactions t
                JOIN accounts a ON t.account_id = a.account_id
                JOIN customers c ON a.customer_id = c.customer_id
                GROUP BY c.customer_id
                ORDER BY islem_sayisi DESC
                LIMIT 1
            """
            cursor.execute(query_active)
            active_user = cursor.fetchone()
            stats['en_aktif_musteri'] = active_user if active_user else None

            # En Çok Para Gönderen Hesap 
            query_sender = """
                SELECT c.name, SUM(t.amount) as toplam_gonderilen
                FROM transactions t
                JOIN accounts a ON t.account_id = a.account_id
                JOIN customers c ON a.customer_id = c.customer_id
                WHERE t.type = 'transfer_out'
                GROUP BY c.customer_id
                ORDER BY toplam_gonderilen DESC
                LIMIT 1
            """
            cursor.execute(query_sender)
            top_sender = cursor.fetchone()
            stats['en_cok_gonderen'] = top_sender if top_sender else None
            
            return stats
        finally:
            conn.close()
    return {}

def get_last_global_transactions(limit=10):
    """Sistemdeki son işlemleri getirir."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                SELECT t.transactions_id, c.name, t.type, t.amount, t.transactions_date
                FROM transactions t
                JOIN accounts a ON t.account_id = a.account_id
                JOIN customers c ON a.customer_id = c.customer_id
                ORDER BY t.transactions_id DESC
                LIMIT ?
            """
            cursor.execute(query, (limit,))
            return cursor.fetchall()
        finally:
            conn.close()
    return []

def get_large_transactions(limit_amount=5000):
    """Belli bir tutarın üzerindeki işlemleri raporlar."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                SELECT c.name, t.type, t.amount
                FROM transactions t
                JOIN accounts a ON t.account_id = a.account_id
                JOIN customers c ON a.customer_id = c.customer_id
                WHERE t.amount >= ?
                ORDER BY t.amount DESC
            """
            cursor.execute(query, (limit_amount,))
            return cursor.fetchall()
        finally:
            conn.close()
    return []