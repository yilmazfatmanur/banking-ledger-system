--manuel balance hesabı (deposit - withdraw)--
SELECT
    a.account_id,
    a.balance AS mevcut_bakiye,
    (SELECT IFNULL(SUM(amount), 0) FROM transactions WHERE account_id = a.account_id AND type = 'deposit') AS total_deposit,
    (SELECT IFNULL(SUM(amount), 0) FROM transactions WHERE account_id = a.account_id AND type = 'withdraw') AS total_withdraw,
    (SELECT IFNULL(SUM(amount), 0) FROM transactions WHERE account_id = a.account_id AND type = 'deposit') -
    (SELECT IFNULL(SUM(amount), 0) FROM transactions WHERE account_id = a.account_id AND type = 'withdraw') AS hesaplanan_bakiye,
    CASE 
        WHEN a.balance = (SELECT IFNULL(SUM(amount), 0) FROM transactions WHERE account_id = a.account_id AND type = 'deposit') -
                         (SELECT IFNULL(SUM(amount), 0) FROM transactions WHERE account_id = a.account_id AND type = 'withdraw')
        THEN 'TUTARLI'
        ELSE 'TUTARSIZ'
    END AS kontrol
FROM accounts a
WHERE a.account_id = 1;