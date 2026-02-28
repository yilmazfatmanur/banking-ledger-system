# test
from anomaly_detector import AnomalyDetector
import os

# Veritabanı yolunu belirt
db_path = os.path.join("..", "bank.db")  
print(f"Kullanılan veritabanı: {db_path}")

detector = AnomalyDetector(db_path)  
onay, risk, message, warning = detector.check_transaction(2, 400, 'withdraw')
print(message)
print(f"İşlem onayı: {'✅' if onay else '❌'}")