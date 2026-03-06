--büyük işlem sorgusu(ana kontrol gibi olması açısından ekledim)--
--1 milyondan büyük işlem kontrolü/test1--
SELECT 
    transactions_id,
    account_id,
    type,
    amount,
    'UYARI: Çok büyük işlem!' AS durum
FROM transactions
WHERE amount >1000000;

--anomaly detactor büyük işlem kontrolü/test2--
--kullanıcının ortalama işleminden 5x büyük işlemler--
SELECT 
    t.transactions_id,
    t.account_id,
    t.type,
    t.amount,
    avg_data.ortalama,
    ROUND(t.amount / avg_data.ortalama, 2) AS kat_farki,
    CASE 
        WHEN t.amount > (avg_data.ortalama * 5) THEN 'ANOMALI - Yuksek Risk'
        WHEN t.amount > (avg_data.ortalama * 3) THEN 'DIKKAT - Orta Risk'
        ELSE 'Normal'
    END AS anomali_durumu
FROM transactions t
JOIN (
    SELECT 
        account_id,
        AVG(amount) AS ortalama,
        COUNT(*) AS islem_sayisi
    FROM transactions
    GROUP BY account_id
    HAVING COUNT(*) >= 3
) avg_data ON t.account_id = avg_data.account_id
WHERE t.amount > (avg_data.ortalama * 3)
ORDER BY kat_farki DESC;

--hesap abzında anomali raporu/test3--
SELECT 
    a.account_id,
    c.name AS musteri_adi,
    COUNT(t.transactions_id) AS toplam_islem,
    ROUND(AVG(t.amount), 2) AS ortalama_tutar,
    MAX(t.amount) AS en_buyuk_islem,
    ROUND(MAX(t.amount) / AVG(t.amount), 2) AS anomali_katsayisi,
    CASE 
        WHEN MAX(t.amount) > AVG(t.amount) * 5 THEN 'Yüksek Risk'
        WHEN MAX(t.amount) > AVG(t.amount) * 3 THEN 'Orta Risk'
        ELSE 'Düşük Risk'
    END AS risk_seviyesi
FROM accounts a
JOIN customers c ON a.customer_id = c.customer_id
LEFT JOIN transactions t ON a.account_id = t.account_id
GROUP BY a.account_id, c.name
HAVING COUNT(t.transactions_id) >= 3
ORDER BY anomali_katsayisi DESC;

--çok küçük işlem kontrolü/test4--
SELECT
    transactions_id,
    account_id,
    type,
    amount
FROM transactions
WHERE amount <= 0;
--beklenen sonuç0--

--bakiye limitleri/test5--
SELECT 
    account_id,
    balance,
    CASE 
        WHEN balance > 10000000 THEN 'Çok Yüksek'
        WHEN balance > 1000000 THEN 'Yüksek'
        WHEN balance < 0 THEN 'HATA: Negatif'
        ELSE 'Normal'
    END AS durum
FROM accounts
WHERE balance > 1000000 OR balance < 0;
