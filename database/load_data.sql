-- Conecta ao banco de dados
\c db_intuitive_care

-- Carrega dados do arquivo de operadoras
\copy operator_registration (Registro_ANS, CNPJ, Razao_Social, Nome_Fantasia, Modalidade, Logradouro, Numero, Complemento, Bairro, Cidade, UF, CEP, DDD, Telefone, Fax, Endereco_eletronico, Representante, Cargo_Representante, Regiao_de_Comercializacao, Data_Registro_ANS) FROM '/home/d2dods/Documentos/Challenge/Intuitive_Challenge/database/resultados/operadoras_ativas.csv' WITH (FORMAT csv, DELIMITER ';', HEADER true, ENCODING 'LATIN1');

-- Criar tabela temporária para carregar os dados brutos
CREATE TEMP TABLE temp_quarterly_balance (
    data DATE,
    reg_ans INTEGER,
    cd_conta_contabil BIGINT,
    descricao TEXT,
    vl_saldo_inicial TEXT,
    vl_saldo_final TEXT
);

-- Carrega dados para a tabela temporária
\copy temp_quarterly_balance FROM '/home/d2dods/Documentos/Challenge/Intuitive_Challenge/database/resultados/demonstracoes_contabeis_combinadas.csv' WITH (FORMAT csv, DELIMITER ';', HEADER true, ENCODING 'LATIN1');

-- Insere os dados na tabela final convertendo as vírgulas para pontos
INSERT INTO quarterly_balance (data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)
SELECT 
    data,
    reg_ans,
    cd_conta_contabil,
    descricao,
    REPLACE(vl_saldo_inicial, ',', '.')::NUMERIC,
    REPLACE(vl_saldo_final, ',', '.')::NUMERIC
FROM temp_quarterly_balance;

-- Remove a tabela temporária
DROP TABLE temp_quarterly_balance;