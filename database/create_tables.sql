-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS db_intuitive_care;

-- Conecta ao banco de dados
\c db_intuitive_care

-- Criação da tabela quarterly_balance
CREATE TABLE IF NOT EXISTS quarterly_balance (
    id SERIAL PRIMARY KEY,
    data DATE NOT NULL,
    reg_ans INTEGER NOT NULL,
    cd_conta_contabil BIGINT NOT NULL,
    descricao TEXT,
    vl_saldo_inicial NUMERIC(18, 2),
    vl_saldo_final NUMERIC(18, 2),
    UNIQUE (data, reg_ans, cd_conta_contabil)
);

-- Criação da tabela cadastro_operadoras
CREATE TABLE IF NOT EXISTS operator_registration (
    id SERIAL PRIMARY KEY,
    Registro_ANS INT,
    CNPJ BIGINT,
    Razao_Social VARCHAR(255),
    Nome_Fantasia VARCHAR(255),
    Modalidade VARCHAR(100),
    Logradouro VARCHAR(255),
    Numero VARCHAR(50),
    Complemento VARCHAR(255),
    Bairro VARCHAR(255),
    Cidade VARCHAR(100),
    UF VARCHAR(2),
    CEP BIGINT,
    DDD FLOAT,
    Telefone FLOAT,
    Fax FLOAT,
    Endereco_eletronico VARCHAR(255),
    Representante VARCHAR(255),
    Cargo_Representante VARCHAR(100),
    Regiao_de_Comercializacao FLOAT,
    Data_Registro_ANS DATE
);