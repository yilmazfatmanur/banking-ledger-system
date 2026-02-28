import numpy as np
import pandas as pd
import sqlite3
from datetime import datetime 
import os

class UserBehaviorProfile:
    """Her kullanıcı için normal davranış profili oluşturur."""

    def __init__(self, account_id, db_path='banka.db'):
        self.account_id = account_id
        self.db_path = db_path
        self.profile = self.build_profile()

    def _get_connection(self):  
        """Veritabanına bağlantı kurar."""
        return sqlite3.connect(self.db_path)
    
    def build_profile(self, limit=50):  
        """Hesabın son işlemlerinden profil oluştur"""
        conn = self._get_connection()
        query = """
        SELECT amount, type
        FROM transactions
        WHERE account_id = ?
        ORDER BY transactions_id DESC
        LIMIT ?
        """
        df = pd.read_sql_query(query, conn, params=(self.account_id, limit))
        conn.close()

        if df.empty or len(df) < 3:
            return None
        
        withdraw_df = df[df['type'] == 'withdraw']
        deposit_df = df[df['type'] == 'deposit']

        profile = {
            'account_id': self.account_id,

            # Tüm işlemler için istatistikler
            'avg_amount': float(df['amount'].mean()) if not df.empty else 0,
            'std_amount': float(df['amount'].std()) if len(df) > 1 else 0,
            'avg_withdraw': float(withdraw_df['amount'].mean()) if not withdraw_df.empty else 0,
            'std_withdraw': float(withdraw_df['amount'].std()) if len(withdraw_df) > 1 else 0,
            'median_amount': float(df['amount'].median()) if not df.empty else 0,
            'max_amount': float(df['amount'].max()) if not df.empty else 0,
            'min_amount': float(df['amount'].min()) if not df.empty else 0,
            'q1_amount': float(df['amount'].quantile(0.25)) if not df.empty else 0,
            'q3_amount': float(df['amount'].quantile(0.75)) if not df.empty else 0,
            'total_transactions': len(df),

            # Çekme işlemleri için istatistikler
            'withdraw_count': len(withdraw_df),
            'withdraw_avg': float(withdraw_df['amount'].mean()) if not withdraw_df.empty else 0,
            'withdraw_max': float(withdraw_df['amount'].max()) if not withdraw_df.empty else 0,

            # Yatırma işlemleri için istatistikler
            'deposit_count': len(deposit_df),
            'deposit_avg': float(deposit_df['amount'].mean()) if not deposit_df.empty else 0,
            'deposit_max': float(deposit_df['amount'].max()) if not deposit_df.empty else 0,
            
            # Dinamik eşikler
            'large_tx_threshold': float(df['amount'].quantile(0.90)) if not df.empty else 0,
            'extreme_tx_threshold': float(df['amount'].mean() + 3 * df['amount'].std()) if len(df) > 1 else float(df['amount'].max() * 2) if not df.empty else 0,
           
            'last_updated': datetime.now().isoformat()
        }
        return profile
    
    def get_risk_score(self, amount, transaction_type):
        """Yeni işlemin risk skorunu hesaplar (0-100)"""
        if self.profile is None:  
            return 20, "Yetersiz işlem geçmişi (en az 3 işlem gerekli!)"
        
        p = self.profile
        risk_score = 0
        reasons = []
        
        # İşlem tipini Türkçe mesajlar için belirle
        islem_tipi_tr = "para çekme" if transaction_type == 'withdraw' else "para yatırma"

        # 1. İşlem türüne göre risk değerlendirmesi
        if transaction_type == 'withdraw':
            if p['withdraw_count'] > 0:
                if amount > p['withdraw_avg'] * 3:
                    risk_score += 30
                    reasons.append(f" normal {islem_tipi_tr} ortalamanızdan 3 katından fazla")
                elif amount > p['withdraw_avg'] * 2:
                    risk_score += 20
                    reasons.append(f" normal {islem_tipi_tr} ortalamanızdan 2 katından fazla")
                elif p['std_withdraw'] > 0 and amount > p['withdraw_avg'] + 2 * p['std_withdraw']:
                    risk_score += 15
                    reasons.append(f" normal {islem_tipi_tr} ortalamanızdan 2 standart sapmadan fazla")
                elif p['std_withdraw'] > 0 and amount > p['withdraw_avg'] + p['std_withdraw']:
                    risk_score += 10
                    reasons.append(f" normal {islem_tipi_tr} ortalamanızdan 1 standart sapmadan fazla")
                elif amount > p['withdraw_avg'] * 1.5:
                    risk_score += 10
                    reasons.append(f" normal {islem_tipi_tr} ortalamanızın üstünde")

                # Maksimum çekme kontrolü
                if amount > p['withdraw_max']:
                    risk_score += 20
                    reasons.append(f" geçmişteki maksimum {islem_tipi_tr} tutarınızdan fazla")
            else:
                risk_score += 25
                reasons.append(f" ilk kez {islem_tipi_tr} işlemi yapıyorsunuz")

        elif transaction_type == 'deposit':
            if p['deposit_count'] > 0:
                if amount > p['deposit_avg'] * 3:
                    risk_score += 25
                    reasons.append(f" normal {islem_tipi_tr} ortalamanızdan 3 katından fazla")
                elif amount > p['deposit_avg'] * 2:
                    risk_score += 20
                    reasons.append(f" normal {islem_tipi_tr} ortalamanızdan 2 katından fazla")
                
                if amount > p['deposit_max']:
                    risk_score += 15
                    reasons.append(f" geçmişteki maksimum {islem_tipi_tr} tutarınızdan fazla")
            else:
                risk_score += 10
                reasons.append(f" ilk kez {islem_tipi_tr} işlemi yapıyorsunuz")
        
        # 2. Tüm işlemlere göre genel kontrol
        if p['std_amount'] > 0:
            z_score = (amount - p['avg_amount']) / p['std_amount']  
            if z_score > 4:  
                risk_score += 25
                reasons.append(" istatistiksel olarak aşırı anormal işlem")
            elif z_score > 3:
                risk_score += 15
                reasons.append(" istatistiksel olarak anormal işlem")

        # 3. Büyük işlem kontrolü 
        if amount > p['extreme_tx_threshold']:
            risk_score += 20
            reasons.append(" aşırı büyük işlem")
        elif amount > p['large_tx_threshold']:
            risk_score += 10
            reasons.append(" büyük işlem")

        # 4. Maksimum işlem kontrolü
        if amount > p['max_amount']:
            risk_score += 15
            reasons.append(" geçmişteki maksimum işlem tutarınızı aşıyor")
        
        # 5. Mevcut bakiye kontrolü
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE account_id = ?", (self.account_id,))
        result = cursor.fetchone()
        conn.close()

        if result and transaction_type == 'withdraw':
            current_balance = result[0]
            if amount > current_balance:
                risk_score += 50
                reasons.append(" mevcut bakiyenizden fazla çekme işlemi")
            elif amount > current_balance * 0.5:
                risk_score += 10
                reasons.append(" mevcut bakiyenizin yarısından fazla çekme işlemi")
        
        risk_score = min(100, risk_score)

        # Risk seviyesini belirle
        if risk_score >= 70:  
            level = "🔴 KRİTİK RİSK"
        elif risk_score >= 50:
            level = "🟠 YÜKSEK RİSK"
        elif risk_score >= 30:
            level = "🟡 ORTA RİSK"
        elif risk_score >= 15:
            level = "🟢 DÜŞÜK RİSK"
        else:
            level = "✅ NORMAL"
        
        message = f"{level} - " + ", ".join(reasons) if reasons else "✅ Bu işlem normal görünüyor."

        return risk_score, message


class AnomalyDetector:
    """Ana anomali tespit sınıfı"""

    def __init__(self, db_path='banka.db'):
        self.db_path = db_path
        self.profiles = {}

    def _get_account_profile(self, account_id):
        """Hesap profili getir"""
        if account_id not in self.profiles:
            self.profiles[account_id] = UserBehaviorProfile(account_id, self.db_path)
        return self.profiles[account_id]
        
    def check_transaction(self, account_id, amount, transaction_type):
        """Yeni işlemi kontrol et ve risk skorunu döndür"""
        profile = self._get_account_profile(account_id)
        
        risk_score, risk_message = profile.get_risk_score(amount, transaction_type)

        # Mevcut bakiye kontrolü
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE account_id = ?", (account_id,)) 
        result = cursor.fetchone()
        conn.close()

        warning = ""
        onay = True

        # Karar mekanizması
        if not result:
            onay = False
            warning = "❌ Hesap bulunamadı, işlem reddedildi."
        elif transaction_type == 'withdraw' and amount > result[0]:
            onay = False
            warning = f"❌ Yetersiz bakiye! Mevcut bakiye: {result[0]} TL"
        elif risk_score >= 70:  
            onay = False
            warning = "❌ Güvenlik nedeniyle işlem reddedildi."
        elif risk_score >= 50:  
            warning = "⚠️ YÜKSEK RİSK! İşlem için onay bekleniyor."
        elif risk_score >= 30:  
            warning = "⚠️ Bu işlem normal alışkanlıklarınızın dışında görünüyor, onay gerekiyor."
        
        final_message = f"Risk Skoru: {risk_score}/100\n{risk_message}\n{warning}" if warning else f"Risk Skoru: {risk_score}/100\n{risk_message}"
        
        return onay, risk_score, final_message, warning
    
    def clear_cache(self):
        """Hesap profili önbelleğini temizle"""
        self.profiles = {}


# Kullanım örneği
if __name__ == "__main__":
    # Veritabanı yolunu ayarla
    db_path = os.path.join("..", "bank.db") if os.path.exists(os.path.join("..", "bank.db")) else 'banka.db'
    detector = AnomalyDetector(db_path)

    account_id = 2
    amount = 400
    transaction_type = 'withdraw'

    onay, risk_score, message, warning = detector.check_transaction(account_id, amount, transaction_type)
    print(message)
    print(f"İşlem onayı: {'✅' if onay else '❌'}")