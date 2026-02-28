# profil testi
from anomaly_detector import UserBehaviorProfile
import sqlite3

# 1. Önce transactions tablosundaki verileri kontrol et
conn = sqlite3.connect('../bank.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM transactions WHERE account_id = 2")
rows = cursor.fetchall()
print(f"Hesap 2 için transactions kayıtları: {len(rows)}")
for row in rows:
    print(f"  {row}")
conn.close()

# 2. Profil oluşturmayı dene
print("\n--- Profil oluşturuluyor ---")
profile = UserBehaviorProfile(2, '../bank.db')
if profile.profile:
    print("✅ Profil oluştu!")
    print(f"Ortalama çekme: {profile.profile.get('withdraw_avg')}")
    print(f"Çekme sayısı: {profile.profile.get('withdraw_count')}")
    print(f"Tüm işlemler: {profile.profile.get('total_transactions')}")
else:
    print("❌ Profil oluşmadı!")
    
    # 3. build_profile fonksiyonunu manuel test et
    print("\n--- Manuel build_profile testi ---")
    conn = profile._get_connection()
    query = """
    SELECT amount, type 
    FROM transactions
    WHERE account_id = ?
    ORDER BY transactions_id DESC
    LIMIT 50
    """
    import pandas as pd
    df = pd.read_sql_query(query, conn, params=(2,))
    conn.close()
    
    print(f"DataFrame satır sayısı: {len(df)}")
    if not df.empty:
        print(df)
    else:
        print("DataFrame BOŞ! transactions tablosunda veri yok.")