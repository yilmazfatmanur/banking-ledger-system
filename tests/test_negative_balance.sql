--negatif bakiye testi--
--negatif bakiyeli hesap kontrolü/test1--
SELECT
    account_id,
    customer_id,
    balance
FROM accounts
WHERE balance < 0;
--beklenen sonuç: negatif bakiyeli hesapların listesi--

--sıfır bakiyeli hesap kontrolü/test2--
SELECT
    account_id,
    customer_id,
    balance
FROM accounts
WHERE balance = 0;
--ps:sıfır olabilir,negatif asla--
