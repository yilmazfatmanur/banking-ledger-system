--sadece depositler--
SELECT * FROM transactions
WHERE type = 'deposit';

--sadece withdrawler--
SELECT * FROM transactions
WHERE type = 'withdraw';

--belirli tutar aralığo--
SELECT * FROM transactions
WHERE amount BETWEEN 100 AND 500;
