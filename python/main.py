from database import create_tables, add_customer, get_customers, create_account, get_accounts, deposit, withdraw, transfer, insert_test_data
import os 

def main():
    print("--- Banka Sistemi Başlatılıyor ---")
    
    # Veritabanı dosyasını kontrol ettirdim (burdan bahsettim mesajda okuduktan sonra bu parantezi sil please)
    db_file = "banka.db"
    if not os.path.exists(db_file):
        print("İlk Çalıştırma: tablolar oluşturuluyor...")
        create_tables()
        print("DB bağlanıyor + tablolar hazır")
    else:
        print("Mevcut veritabanı yüklendi...")
    
    while True:
        print("\n--- ANA MENÜ ---")
        print("1. Müşteri Ekle")
        print("2. Hesap Oluştur")
        print("3. Hesapları Listele")
        print("4. Para Yatırma (Deposit)")
        print("5. Para Çekme (Withdraw)")
        print("6. Para Transferi")
        print("7. Test Verileri Ekle")
        print("8. Çıkış")

        
        secim = input("Seçiminiz: ")
        
        if secim == "1":
            print("\n--- Yeni Müşteri Ekle ---")
            isim = input("Müşteri Adı Soyadı: ")
            if isim.strip():
                add_customer(isim)
            else:
                print("İsim boş olamaz!")

        #get customers (hesap oluşturma)
        elif secim == "2":
            print("\n--- HESAP OLUŞTURMA ---")
            musteriler = get_customers()
            if not musteriler:
                print("Müşteri yok. Önce 1. menüden müşteri ekleyin.")
            else:
                for m in musteriler:
                    print(f"ID: {m['customer_id']} - İsim: {m['name']}")
                try:
                    secilen_id = int(input("\nHesap açılacak Müşteri ID: "))
                    create_account(secilen_id)
                except ValueError:
                    print("HATA: Geçerli bir sayı girin!")

        # get accounts (hesap listesi)
        elif secim == "3":
            print("\n--- HESAP LİSTESİ ---")
            hesaplar = get_accounts()
            if not hesaplar:
                print("Sistemde hesap yok.")
            else:
                print(f"{'Hesap No':<10} | {'Müşteri Adı':<20} | {'Bakiye':<10}")
                print("-" * 45)
                for h in hesaplar:
                    print(f"{h['hesap_no']:<10} | {h['musteri_adi']:<20} | {h['bakiye']} TL")

        # deposit (para yatırma)
        elif secim == "4":
            print("\n--- PARA YATIRMA ---")
            try:
                hesap_id = int(input("Para yatırılacak Hesap No: "))
                tutar = float(input("Yatırılacak Tutar (TL): "))
                if tutar > 0:
                    deposit(hesap_id, tutar)
                else:
                    print("HATA: Tutar 0'dan büyük olmalıdır.")
            except ValueError:
                print("HATA: Lütfen geçerli sayılar girin!")

        #withdraw (para çekme)
        elif secim == "5":
            print("\n--- PARA ÇEKME ---")
            try:
                hesap_id = int(input("Para çekilecek Hesap No: "))
                tutar = float(input("Çekilecek Tutar (TL): "))
                if tutar > 0:
                    withdraw(hesap_id, tutar)
                else:
                    print("HATA: Tutar 0'dan büyük olmalıdır.")
            except ValueError:
                print("HATA: Lütfen geçerli sayılar girin!")

        elif secim == "6":
            print("\n--- PARA TRANSFERİ---")
            try:
                from_account_id = int(input("Transfer yapılacak Hesap No: "))
                to_account_id = int(input("Transfer edilecek Hesap No: "))
                tutar = float(input("Transfer Edilecek Tutar (TL): "))
                if tutar > 0:
                    transfer(from_account_id, to_account_id, tutar)
                else:
                    print("HATA: Tutar 0'dan büyük olmalıdır.")
            except ValueError:
                print("HATA: Lütfen geçerli sayılar girin!")
        
        elif secim == "7":
            insert_test_data()

    
        elif secim == "8":
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim. Lütfen 1-8 arasında bir sayı girin.")

if __name__ == "__main__":
    main()
