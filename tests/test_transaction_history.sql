--hesabın işlem geçmişi--
SELECT 
    transaction_id,
    type,
    amount,
    strftime('%d.%m.%Y %H:%M', created_at) AS tarih,
    description
FROM transactions
WHERE account_id = ?
ORDER BY created_at DESC;