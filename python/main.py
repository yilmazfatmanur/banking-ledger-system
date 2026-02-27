from database import create_tables, add_customer, get_customers, create_account, get_accounts, deposit, withdraw, transfer, insert_test_data, DB_PATH, get_transaction_history, get_bank_summary
import os

def main():
    print("--- Banka Sistemi Başlatılıyor ---")

    db_file = "../bank.db"
    if not os.path.exists(db_file):
        print("İlk Çalıştırma: tablolar oluşturuluyor...")
        create_tables()
        print("DB bağlanıyor + tablolar hazır")
    else:
        print("Mevcut veritabanı yüklendi...")
    
    while True:
        print("--- ANA MENÜ ---")
        print("1. Müşteri Ekle")
        print("2. Hesap Oluştur")
        print("3. Hesapları Listele")
        print("4. Para Yatırma (Deposit)")
        print("5. Para Çekme (Withdraw)")
        print("6. Para Transferi")
        print("7. Test Verileri Ekle")
        print("8. Raporları Görüntüle")
        print("9. Çıkış")

        
        secim = input("Seçiminiz: ")
        
        #müşteri ekleme
        if secim == "1":
            while True:
                print("\n--- Yeni Müşteri Ekle ---")
                isim = input("Müşteri Adı Soyadı: ")
                if isim.strip():
                    add_customer(isim)
                else:
                    print("İsim boş olamaz!")

                tekrar = input("\nBaşka bir müşteri eklemek ister misiniz? (E/H): ") .strip().upper()
                if tekrar != 'E':
                    break

        #get customers (hesap oluşturma)
        elif secim == "2":
            while True:
                print("\n--- Hesap Oluşturma ---")
                musteriler = get_customers()
                if not musteriler:
                    print("Müşteri yok. Önce 1. menüden müşteri ekleyin.")
                    break
                else:
                    for m in musteriler:
                        print(f"ID: {m['customer_id']} - İsim: {m['name']}")
                    try:
                        secilen_id = int(input("\nHesap açılacak Müşteri ID: "))
                        create_account(secilen_id)
                    except ValueError:
                        print("HATA: Geçerli bir sayı girin!")
                tekrar = input("\nBaşka bir hesap oluşturmak ister misiniz? (E/H): ") .strip().upper()
                if tekrar != 'E':
                    break

        # get accounts (hesap listesi)
        elif secim == "3":
            print("\n--- Hesap Listesi ---")
            hesaplar = get_accounts()
            if not hesaplar:
                print("Sistemde hesap yok.")
            else:
                print(f"{'Hesap No':<10} | {'Müşteri Adı':<20} | {'Bakiye':<10}")
                print("-" * 45)
                for h in hesaplar:
                    print(f"{h['hesap_no']:<10} | {h['musteri_adi']:<20} | {h['bakiye']} TL")

            input("\n Ana menüye dönmek için 'Enter' tuşuna basın...")

        # deposit (para yatırma)
        elif secim == "4":
            while True:
                print("\n--- Para Yatırma ---")
                try:
                    hesap_id = int(input("Para yatırılacak Hesap No: "))
                    tutar = float(input("Yatırılacak Tutar (TL): "))
                    if tutar > 0:
                        deposit(hesap_id, tutar)
                    else:
                        print("HATA: Tutar 0'dan büyük olmalıdır.")
                except ValueError:
                    print("HATA: Lütfen geçerli sayılar girin!")

                tekrar = input("\nBaşka bir para yatırma işlemi yapmak ister misiniz? (E/H): ") .strip().upper()
                if tekrar != 'E':
                    break

        #withdraw (para çekme)
        elif secim == "5":
            while True:
                print("\n--- Para Çekme ---")
                try:
                    hesap_id = int(input("Para çekilecek Hesap No: "))
                    tutar = float(input("Çekilecek Tutar (TL): "))
                    if tutar > 0:
                        withdraw(hesap_id, tutar)
                    else:
                        print("HATA: Tutar 0'dan büyük olmalıdır.")
                except ValueError:
                    print("HATA: Lütfen geçerli sayılar girin!")
                
                tekrar = input("\nTekrar para çekme işlemi yapmak ister misiniz? (E/H): ") .strip().upper()
                if tekrar != 'E':
                        break

            
        # transaction (para transferi)
        elif secim == "6":
            while True:
                print("\n--- Para Transferi ---")
                try:
                    from_account_id = int(input("Gönderen Hesap No: "))
                    to_account_id = int(input("Alıcı Hesap No: "))
                    tutar = float(input("Transfer Edilecek Tutar (TL): "))
                    if tutar > 0:
                        transfer(from_account_id, to_account_id, tutar)
                    else:
                        print("HATA: Tutar 0'dan büyük olmalıdır.")
                except ValueError:
                    print("HATA: Lütfen geçerli sayılar girin!")
                
                tekrar = input("\nBaşka para transferi yapmak ister misiniz? (E/H): ") .strip().upper()
                if tekrar != 'E':
                    break

        # test verisi ekleme
        elif secim == "7":
            insert_test_data()
            input("\nAna menüye dönmek için 'Enter' tuşuna basın...")

        # raporlar
        elif secim == "8":
            while True:
                print("\n--- RAPORLAR MENÜSÜ ---")
                print("1. Belirli Bir Hesabın İşlem Geçmişi")
                print("2. Banka Genel Özeti")
                print("3. Ana Menüye Dön")
                rapor_secim = input("Görmek istediğiniz raporu seçin: ")
                
                if rapor_secim == "1":
                    try:
                        hesap_id = int(input("\nİşlem geçmişi istenen Hesap No: "))
                        gecmis = get_transaction_history(hesap_id)
                        
                        if gecmis:
                            print(f"\n--- Hesap No: {hesap_id} İşlem Geçmişi ---")
                            print(f"{'İşlem ID':<10} | {'İşlem Tipi':<15} | {'Tutar':<10} | {'Bakiye':<10}")
                            print("-" * 55)
                            for g in gecmis:
                                print(f"{g['transactions_id']:<10} | {g['islem_tipi']:<15} | {g['tutar']:<10} | {g['guncel_bakiye']} TL")
                        else:
                            print("Bu hesaba ait herhangi bir işlem bulunamadı veya hesap yok.")
                    except ValueError:
                        print("HATA: Lütfen geçerli bir Hesap No girin!")
                        
                elif rapor_secim == "2":
                    ozet = get_bank_summary()
                    print("\n" + "*"*30)
                    print("   BANKA GENEL DURUM ÖZETİ   ")
                    print("*"*30)
                    print(f"Sistemdeki Toplam Müşteri : {ozet['musteri_sayisi']}")
                    print(f"Açılan Toplam Hesap Sayısı: {ozet['hesap_sayisi']}")
                    print(f"Bankadaki Toplam Mevduat  : {ozet['toplam_bakiye']} TL")
                    print(f"Gerçekleşen Toplam İşlem  : {ozet['islem_sayisi']}")
                    print("*"*30)
                    
                elif rapor_secim == "3":
                    break
                else:
                    print("Geçersiz seçim! Lütfen 1-3 arası bir değer girin.")
    
        # çıkış
        elif secim == "9":
            print("Banka sisteminden çıkış yapılıyor... İyi günler!")
            break 
            
        else:
            print("Geçersiz seçim. Lütfen 1-9 arasında bir sayı girin.")
            input("\nDevam etmek için 'Enter' tuşuna basın...")

if __name__ == "__main__":
    main()