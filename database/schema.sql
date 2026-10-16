
-- ============================================================
-- BANCO DE DADOS - PL MIL TRANSPORTES
-- Estrutura atual da aplicação
-- ============================================================

CREATE TABLE empresa (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL
);

CREATE TABLE motorista (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    valor_km NUMERIC(10, 2) NOT NULL
);

CREATE TABLE funcionario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    empresa_id INTEGER NOT NULL,
    CONSTRAINT fk_funcionario_empresa
        FOREIGN KEY (empresa_id)
        REFERENCES empresa(id)
);

CREATE TABLE servico (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER NOT NULL,
    motorista_id INTEGER NOT NULL,
    data DATE NOT NULL,
    km NUMERIC(10, 2) NOT NULL,
    valor_km_motorista NUMERIC(10, 2) NOT NULL,

    CONSTRAINT fk_servico_empresa
        FOREIGN KEY (empresa_id)
        REFERENCES empresa(id),

    CONSTRAINT fk_servico_motorista
        FOREIGN KEY (motorista_id)
        REFERENCES motorista(id)
);

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

CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    perfil VARCHAR(20) NOT NULL DEFAULT 'OPERADOR',
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_usuario_perfil
        CHECK (perfil IN ('ADMINISTRADOR', 'OPERADOR'))
);
