-- 10 operadoras com maiores despesas no último trimestre
WITH ultimo_trimestre AS (
    SELECT MAX(data) as ultima_data
    FROM quarterly_balance
)
SELECT DISTINCT
    CONVERT_FROM(CONVERT_TO(co.Razao_Social, 'LATIN1'), 'UTF8') as Razao_Social,
    co.Nome_Fantasia,
    co.Registro_ANS,
    ABS(qb.vl_saldo_final) as despesa_total
FROM quarterly_balance qb
JOIN cadastro_operadoras co ON qb.reg_ans = co.Registro_ANS
JOIN ultimo_trimestre ut ON qb.data = ut.ultima_data
WHERE qb.descricao LIKE 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS%'
ORDER BY ABS(qb.vl_saldo_final) DESC
LIMIT 10;

-- 10 operadoras com maiores despesas no último ano
WITH datas_ano AS (
    SELECT 
        MAX(data) as data_fim,
        MAX(data) - INTERVAL '1 year' as data_inicio
    FROM quarterly_balance
)
SELECT DISTINCT
    CONVERT_FROM(CONVERT_TO(co.Razao_Social, 'LATIN1'), 'UTF8') as Razao_Social,
    co.Nome_Fantasia,
    co.Registro_ANS,
    ABS(SUM(qb.vl_saldo_final)) as despesa_total_anual
FROM quarterly_balance qb
JOIN cadastro_operadoras co ON qb.reg_ans = co.Registro_ANS
JOIN datas_ano da ON qb.data > da.data_inicio AND qb.data <= da.data_fim
WHERE qb.descricao LIKE 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS%'
GROUP BY co.Razao_Social, co.Nome_Fantasia, co.Registro_ANS
ORDER BY despesa_total_anual DESC
LIMIT 10;