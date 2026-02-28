--deposit transaction test--
--son deposit işleminin transaction kaydı--
SELECT 
    transactions_id,
    account_id,
    type,
    amount
FROM transactions
WHERE account_id = 2 AND type = 'deposit'
ORDER BY transactions_id DESC
LIMIT 1;