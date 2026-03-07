from anomaly_detector import AnomalyDetector
from database import (
    create_tables, add_customer, get_customers, create_account, 
    get_accounts, deposit, withdraw, transfer, insert_test_data, 
    DB_PATH, get_transaction_history, get_bank_summary, 
    get_active_stats, get_last_global_transactions, get_large_transactions )
import os
from decimal import Decimal

def main():
    print("--- Banka Sistemi Başlatılıyor ---")

    if not os.path.exists(DB_PATH):
            print(" Veritabanı ve tablolar oluşturuluyor...")
            create_tables()
            print("Veritabanı hazır.")
    else:
            print(" Veritabanı yüklendi: {DB_PATH}")
        
    detector = AnomalyDetector(DB_PATH)
        
    while True:
        print("\n--- ANA MENÜ ---")
        print("1. Müşteri Ekle")
        print("2. Hesap Oluştur")
        print("3. Hesapları Listele")
        print("4. Para Yatırma (Deposit)")
        print("5. Para Çekme (Withdraw)")
        print("6. Para Transferi")
        print("7. Test Verileri Ekle")
        print("8. Raporları Görüntüle")
        print("9. Akıllı İşlem Tespiti")
        print("10. Hesap Ekstresi")
        print("11. Çıkış")
        
        secim = input("Seçiminiz: ")
        
       
        if secim == "1":
            while True:
                print("\n--- Yeni Müşteri Ekle ---")
                isim = input("Müşteri Adı Soyadı: ")
                if isim.strip():
                    add_customer(isim)
                else:
                    print("İsim boş olamaz!")

                tekrar = input("\nBaşka bir müşteri eklemek ister misiniz? (E/H): ").strip().upper()
                if tekrar != 'E':
                    break

      
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
                tekrar = input("\nBaşka bir hesap oluşturmak ister misiniz? (E/H): ").strip().upper()
                if tekrar != 'E':
                    break

        
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

            input("\nAna menüye dönmek için 'Enter' tuşuna basın...")

      
        elif secim == "4":
            while True:
                print("\n--- Para Yatırma ---")
                try:
                    hesap_id = int(input("Para yatırılacak Hesap No: "))
                    tutar = Decimal(input("Yatırılacak Tutar (TL): "))
                    if tutar > 0:
                        deposit(hesap_id, tutar)
                    else:
                        print("HATA: Tutar 0'dan büyük olmalıdır.")
                except ValueError:
                    print("HATA: Lütfen geçerli sayılar girin!")

                tekrar = input("\nBaşka bir para yatırma işlemi yapmak ister misiniz? (E/H): ").strip().upper()
                if tekrar != 'E':
                    break

       
        elif secim == "5":
            while True:
                print("\n--- Para Çekme ---")
                try:
                    hesap_id = int(input("Para çekilecek Hesap No: "))
                    tutar = Decimal(input("Çekilecek Tutar (TL): "))
                    if tutar > 0:
                        withdraw(hesap_id, tutar)
                    else:
                        print("HATA: Tutar 0'dan büyük olmalıdır.")
                except ValueError:
                    print("HATA: Lütfen geçerli sayılar girin!")
                
                tekrar = input("\nTekrar para çekme işlemi yapmak ister misiniz? (E/H): ").strip().upper()
                if tekrar != 'E':
                    break


        elif secim == "6":
            while True:
                print("\n--- Para Transferi ---")
                try:
                    from_account_id = int(input("Gönderen Hesap No: "))
                    to_account_id = int(input("Alıcı Hesap No: "))
                    tutar = Decimal(input("Transfer Edilecek Tutar (TL): "))
                    if tutar > 0:
                        transfer(from_account_id, to_account_id, tutar)
                    else:
                        print("HATA: Tutar 0'dan büyük olmalıdır.")
                except ValueError:
                    print("HATA: Lütfen geçerli sayılar girin!")
                
                tekrar = input("\nBaşka para transferi yapmak ister misiniz? (E/H): ").strip().upper()
                if tekrar != 'E':
                    break

       
        elif secim == "7":
            insert_test_data()
            input("\nAna menüye dönmek için 'Enter' tuşuna basın...")

       
        elif secim == "8":
            print("\n" + "="*40)
            print("      BANKA YÖNETİCİ RAPORU")
            print("="*40)
            
            # GENEL ÖZET
            ozet = get_bank_summary()
            print(f"\n[GENEL DURUM]")
            print(f"Müşteri Sayısı    : {ozet.get('musteri_sayisi', 0)}")
            print(f"Hesap Sayısı      : {ozet.get('hesap_sayisi', 0)}")
            print(f"Bankadaki Toplam  : {ozet.get('toplam_para', 0):,.2f} TL")
            print(f"Toplam Yatırılan  : {ozet.get('toplam_yatirilan', 0):,.2f} TL  (✅)")
            print(f"Toplam Çekilen    : {ozet.get('toplam_cekilen', 0):,.2f} TL    (🔻)")

            # Analiz
            istatistik = get_active_stats()
            print(f"\n[EN'LER]")
            
            aktif = istatistik.get('en_aktif_musteri')
            if aktif:
                print(f"🏆 En Aktif Müşteri : {aktif['name']} ({aktif['islem_sayisi']} işlem)")
            else:
                print("🏆 En Aktif Müşteri : Veri yok")

            zengin = istatistik.get('en_cok_gonderen')
            if zengin:
                print(f"💸 En Çok Gönderen  : {zengin['name']} (Toplam {zengin['toplam_gonderilen']:,.2f} TL transfer)")
            else:
                print("💸 En Çok Gönderen  : Veri yok")

            # anomali Raporu
            print(f"\n[⚠️ BÜYÜK İŞLEM UYARILARI (>5.000 TL)]")
            buyuk_islemler = get_large_transactions(5000)
            if buyuk_islemler:
                for b in buyuk_islemler:
                    print(f"  - {b['name']} | {b['type']} | {b['amount']:,.2f} TL")
            else:
                print("  - Kritik seviyede büyük işlem bulunamadı.")

            
            print(f"\n[⏱️ SON 10 İŞLEM]")
            son_islemler = get_last_global_transactions(10)
            print(f"{'Zaman':<20} | {'Müşteri':<15} | {'Tip':<12} | {'Tutar'}")
            print("-" * 60)
            for isl in son_islemler:
                # tarih formatını temizle varsa
                tarih = isl['transactions_date'] if isl['transactions_date'] else "N/A"
                print(f"{tarih:<20} | {isl['name']:<15} | {isl['type']:<12} | {isl['amount']} TL")
            
            input("\nMenüye dönmek için Enter'a basın...")
    
        elif secim == "9":
            print("\n--- Akıllı İşlem Tespiti ---")
            try:
                account_id = int(input("İşlem yapılacak Hesap No: "))
                tutar = Decimal(input("İşlem Tutarı: "))
                islem_tipi = input("İşlem Tipi (yatırma/çekme): ").lower()

                if islem_tipi in ['yatırma', 'deposit', 'y']:
                    islem_tipi = 'deposit'
                elif islem_tipi in ['çekme', 'withdraw', 'c']:
                    islem_tipi = 'withdraw'
                else:
                    print("HATA: Geçersiz işlem tipi! (yatırma veya çekme yazın)")
                    continue

                # detector kontrolü
                onay, risk, message, warning = detector.check_transaction(account_id, tutar, islem_tipi)
                
                print(f"\n{message}")
                
                if warning:
                    print(f"⚠️ {warning}")

                if onay:
                    if islem_tipi == 'withdraw':
                        withdraw(account_id, tutar)
                    else:
                        deposit(account_id, tutar)
                    print(" İşlem başarıyla gerçekleştirildi!")
                else:
                    print(" İşlem gerçekleştirilmedi!")
                    
            except ValueError:
                print("HATA: Lütfen geçerli sayılar girin!")
            except Exception as e:
                print(f"HATA: {str(e)}")

        
        elif secim == "10":
            print("\n--- HESAP EKSTRESİ ---")
            try:
                h_id = int(input("Ekstresi istenen Hesap No: "))
                gecmis = get_transaction_history(h_id)
                
                if not gecmis:
                    print("Bu hesaba ait geçmiş işlem bulunamadı.")
                else:
                    print(f"\n{'ID':<5} | {'Tip':<12} | {'Tutar':<15} | {'Bakiye'}")
                    print("-" * 50)
                    for islem in gecmis:
                        # database.py'dan gelen veriyi ayrıştırma
                        t_id = islem['transactions_id']
                        t_tip = islem['islem_tipi']
                        
                        t_tutar = f"{islem['tutar']} TL"
                        t_bakiye = f"{islem['guncel_bakiye']} TL"
                        
                        print(f"{t_id:<5} | {t_tip:<12} | {t_tutar:<15} | {t_bakiye}")
                        
            except ValueError:
                print(" Hata: Geçerli bir sayı girin.")
            
            input("\nMenüye dönmek için Enter'a basın...")


        
        elif secim == "11":
            print("Banka sisteminden çıkış yapılıyor... İyi günler!")
            break 
            
        else:
            print("Geçersiz seçim. Lütfen 1-10 arasında bir sayı girin.")
            input("\nDevam etmek için 'Enter' tuşuna basın...")

if __name__ == "__main__":
    main()