--deposit ledger test--
--son deposit işleminin ledger kaydı--
SELECT
    l.ledger_id,
    l.transactions_id,
    l.debit_account,
    l.credit_account,
    l.amount,
    t.type
FROM ledger l
JOIN transactions t ON l.transactions_id = t.transactions_id
WHERE t.type = 'deposit' AND t.account_id = 2
ORDER BY l.ledger_id DESC
LIMIT 1;