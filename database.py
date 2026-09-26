import os

import psycopg2
from dotenv import load_dotenv


load_dotenv()


def conectar_banco():
    conexao = psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        database="plmil",
        user="postgres",
        password=os.getenv("DB_PASSWORD")
    )

    return conexao


def buscar_empresas():
    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            nome
        FROM empresa
        ORDER BY id;
    """)

    empresas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return empresas


def inserir_empresa(nome):
    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO empresa (nome)
        VALUES (%s);
        """,
        (nome,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()


def buscar_motoristas():
    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id,
            nome,
            valor_km
        FROM motorista
        ORDER BY id;
    """)

    motoristas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return motoristas


def inserir_motorista(nome, valor_km):
    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO motorista (
            nome,
            valor_km
        )
        VALUES (%s, %s);
        """,
        (
            nome,
            valor_km
        )
    )

    conexao.commit()

    cursor.close()
    conexao.close()


def buscar_funcionarios():
    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            f.id,
            f.nome,
            e.nome
        FROM funcionario f
        JOIN empresa e
            ON f.empresa_id = e.id
        ORDER BY f.id;
    """)

    funcionarios = cursor.fetchall()

    cursor.close()
    conexao.close()

    return funcionarios


def buscar_funcionarios_por_empresa(empresa_id):
    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            id,
            nome
        FROM funcionario
        WHERE empresa_id = %s
        ORDER BY nome;
        """,
        (empresa_id,)
    )

    funcionarios = cursor.fetchall()

    cursor.close()
    conexao.close()

    return funcionarios


def inserir_funcionario(nome, empresa_id):
    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO funcionario (
            nome,
            empresa_id
        )
        VALUES (%s, %s);
        """,
        (
            nome,
            empresa_id
        )
    )

    conexao.commit()

    cursor.close()
    conexao.close()


def buscar_servicos():
    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            s.id,
            e.nome,
            m.nome,
            s.data,
            s.km,
            s.valor_km_motorista,
            s.km * s.valor_km_motorista AS valor_motorista,

            COALESCE(
                STRING_AGG(
                    f.nome,
                    ', '
                    ORDER BY f.nome
                ),
                'Nenhum funcionário'
            ) AS funcionarios

        FROM servico s

        JOIN empresa e
            ON s.empresa_id = e.id

        JOIN motorista m
            ON s.motorista_id = m.id

        LEFT JOIN servico_funcionario sf
            ON s.id = sf.servico_id

        LEFT JOIN funcionario f
            ON sf.funcionario_id = f.id

        GROUP BY
            s.id,
            e.nome,
            m.nome,
            s.data,
            s.km,
            s.valor_km_motorista

        ORDER BY s.id;
    """)

    servicos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return servicos


def inserir_servico(
    empresa_id,
    motorista_id,
    data,
    km,
    funcionarios_ids
):
    conexao = conectar_banco()

    cursor = conexao.cursor()

    if not funcionarios_ids:
        cursor.close()
        conexao.close()

        raise ValueError(
            "O serviço precisa ter pelo menos um funcionário."
        )

    cursor.execute(
        """
        SELECT
            valor_km
        FROM motorista
        WHERE id = %s;
        """,
        (motorista_id,)
    )

    resultado = cursor.fetchone()

    if resultado is None:
        cursor.close()
        conexao.close()

        raise ValueError("Motorista não encontrado.")

    valor_km_motorista = resultado[0]

    funcionarios_ids = [
        int(funcionario_id)
        for funcionario_id in funcionarios_ids
    ]

    cursor.execute(
        """
        SELECT
            id
        FROM funcionario
        WHERE empresa_id = %s
        AND id = ANY(%s);
        """,
        (
            empresa_id,
            funcionarios_ids
        )
    )

    funcionarios_validos = {
        funcionario[0]
        for funcionario in cursor.fetchall()
    }

    if len(funcionarios_validos) != len(set(funcionarios_ids)):
        cursor.close()
        conexao.close()

        raise ValueError(
            "Um ou mais funcionários não pertencem à empresa selecionada."
        )

    cursor.execute(
        """
        INSERT INTO servico (
            empresa_id,
            motorista_id,
            data,
            km,
            valor_km_motorista
        )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """,
        (
            empresa_id,
            motorista_id,
            data,
            km,
            valor_km_motorista
        )
    )

    servico_id = cursor.fetchone()[0]

    for funcionario_id in funcionarios_ids:

        cursor.execute(
            """
            INSERT INTO servico_funcionario (
                servico_id,
                funcionario_id
            )
            VALUES (%s, %s);
            """,
            (
                servico_id,
                funcionario_id
            )
        )

    conexao.commit()

    cursor.close()
    conexao.close()