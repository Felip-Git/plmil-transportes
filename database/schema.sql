-- =========================================
-- BANCO DE DADOS - PL MIL TRANSPORTES
-- =========================================

-- =========================================
-- EMPRESAS
-- =========================================

CREATE TABLE empresa (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL
);


-- =========================================
-- MOTORISTAS
-- =========================================

CREATE TABLE motorista (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL
);


-- =========================================
-- FUNCIONÁRIOS
-- =========================================

CREATE TABLE funcionario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL
);


-- =========================================
-- PEDIDOS
-- =========================================

CREATE TABLE pedido (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER NOT NULL,
    data_criacao DATE NOT NULL DEFAULT CURRENT_DATE,

    CONSTRAINT fk_pedido_empresa
        FOREIGN KEY (empresa_id)
        REFERENCES empresa(id)
);


-- =========================================
-- SERVIÇOS
-- =========================================

CREATE TABLE servico (
    id SERIAL PRIMARY KEY,
    pedido_id INTEGER NOT NULL,
    motorista_id INTEGER NOT NULL,
    data DATE NOT NULL,
    km NUMERIC(10,2) NOT NULL,
    valor_km_motorista NUMERIC(10,2) NOT NULL,

    CONSTRAINT fk_servico_pedido
        FOREIGN KEY (pedido_id)
        REFERENCES pedido(id),

    CONSTRAINT fk_servico_motorista
        FOREIGN KEY (motorista_id)
        REFERENCES motorista(id)
);


-- =========================================
-- RELAÇÃO SERVIÇO ↔ FUNCIONÁRIO
-- =========================================

CREATE TABLE servico_funcionario (
    servico_id INTEGER NOT NULL,
    funcionario_id INTEGER NOT NULL,

    PRIMARY KEY (servico_id, funcionario_id),

    CONSTRAINT fk_servico_funcionario_servico
        FOREIGN KEY (servico_id)
        REFERENCES servico(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_servico_funcionario_funcionario
        FOREIGN KEY (funcionario_id)
        REFERENCES funcionario(id)
        ON DELETE CASCADE
);