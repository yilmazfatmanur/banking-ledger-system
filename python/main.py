from database import create_tables, add_customer

def main():
    print("--- Banking Ledger System Başlatılıyor ---")
    
    # Tabloları kur (Verileri sıfırlar!)
    create_tables()
    print("DB bağlanıyor + tablolar hazır")

    while True:
        print("\n--- ANA MENÜ ---")
        print("1. Müşteri Ekle")
        print("2. Çıkış")
        
        secim = input("Seçiminiz: ")
        
        if secim == "1":
            print("\n--- Yeni Müşteri Ekle ---")
            # İSİM İSTEME
            isim = input("Müşteri Adı Soyadı: ")
            
            if isim.strip(): # İsim doluysa
                add_customer(isim)
                # pydan EKLEME MESAJI
                print("Python’dan müşteri ekleniyor... ")
            else:
                print("İsim boş olamaz!")
            
        elif secim == "2":
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim.")

if __name__ == "__main__":
    main()