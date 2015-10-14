 SELECT l.id,
        l.date,
        CASE WHEN ai.id IS NOT NULL THEN CASE WHEN ai.type in ('out_refund','in_refund') THEN -1*ai.residual ELSE ai.residual END ELSE l.debit - l.credit END as balance, ai.origin as inv_num,
        CASE WHEN ai.id is not NULL THEN ai.date_due ELSE l.date_maturity END as date_due, ai.amount_untaxed,
        j.code,
        acc.code as a_code,
        acc.name as a_name,
        l.ref,
        m.name as move_name,
        l.name,
        l.debit,
        l.credit,
        l.amount_currency,
        l.currency_id,
        c.symbol AS currency_code
FROM account_move_line l
LEFT JOIN account_invoice as ai ON ai.move_id = l.move_id
LEFT JOIN account_journal j ON (l.journal_id = j.id)
LEFT JOIN account_account acc ON (l.account_id = acc.id)
LEFT JOIN res_currency c ON (l.currency_id=c.id)
LEFT JOIN account_move m ON (m.id=l.move_id)
WHERE l.partner_id = %s
AND l.account_id IN %s AND " + self.query +"
AND m.state IN %s RECONCILE_TAG
ORDER BY l.date