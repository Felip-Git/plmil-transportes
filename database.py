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


# ============================================================
# EMPRESAS
# ============================================================

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


def buscar_empresa_por_id(empresa_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            id,
            nome
        FROM empresa
        WHERE id = %s;
        """,
        (empresa_id,)
    )

    empresa = cursor.fetchone()

    cursor.close()
    conexao.close()

    return empresa


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


def atualizar_empresa(empresa_id, nome):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE empresa
        SET nome = %s
        WHERE id = %s;
        """,
        (
            nome,
            empresa_id
        )
    )

    conexao.commit()

    cursor.close()
    conexao.close()


def excluir_empresa(empresa_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM funcionario
        WHERE empresa_id = %s;
        """,
        (empresa_id,)
    )

    quantidade_funcionarios = cursor.fetchone()[0]

    if quantidade_funcionarios > 0:
        cursor.close()
        conexao.close()

        raise ValueError(
            "Não é possível excluir esta empresa porque existem "
            "funcionários vinculados a ela."
        )

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM servico
        WHERE empresa_id = %s;
        """,
        (empresa_id,)
    )

    quantidade_servicos = cursor.fetchone()[0]

    if quantidade_servicos > 0:
        cursor.close()
        conexao.close()

        raise ValueError(
            "Não é possível excluir esta empresa porque existem "
            "serviços vinculados a ela."
        )

    cursor.execute(
        """
        DELETE FROM empresa
        WHERE id = %s;
        """,
        (empresa_id,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()


# ============================================================
# MOTORISTAS
# ============================================================

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


def buscar_motorista_por_id(motorista_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            id,
            nome,
            valor_km
        FROM motorista
        WHERE id = %s;
        """,
        (motorista_id,)
    )

    motorista = cursor.fetchone()

    cursor.close()
    conexao.close()

    return motorista


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


def atualizar_motorista(
    motorista_id,
    nome,
    valor_km
):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE motorista
        SET
            nome = %s,
            valor_km = %s
        WHERE id = %s;
        """,
        (
            nome,
            valor_km,
            motorista_id
        )
    )

    conexao.commit()

    cursor.close()
    conexao.close()


def excluir_motorista(motorista_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM servico
        WHERE motorista_id = %s;
        """,
        (motorista_id,)
    )

    quantidade_servicos = cursor.fetchone()[0]

    if quantidade_servicos > 0:
        cursor.close()
        conexao.close()

        raise ValueError(
            "Não é possível excluir este motorista porque existem "
            "serviços vinculados a ele."
        )

    cursor.execute(
        """
        DELETE FROM motorista
        WHERE id = %s;
        """,
        (motorista_id,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()


# ============================================================
# FUNCIONÁRIOS
# ============================================================

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


def buscar_funcionario_por_id(funcionario_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            id,
            nome,
            empresa_id
        FROM funcionario
        WHERE id = %s;
        """,
        (funcionario_id,)
    )

    funcionario = cursor.fetchone()

    cursor.close()
    conexao.close()

    return funcionario


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


def atualizar_funcionario(
    funcionario_id,
    nome,
    empresa_id
):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE funcionario
        SET
            nome = %s,
            empresa_id = %s
        WHERE id = %s;
        """,
        (
            nome,
            empresa_id,
            funcionario_id
        )
    )

    conexao.commit()

    cursor.close()
    conexao.close()


def excluir_funcionario(funcionario_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM servico_funcionario
        WHERE funcionario_id = %s;
        """,
        (funcionario_id,)
    )

    quantidade_servicos = cursor.fetchone()[0]

    if quantidade_servicos > 0:
        cursor.close()
        conexao.close()

        raise ValueError(
            "Não é possível excluir este funcionário porque existem "
            "serviços vinculados a ele."
        )

    cursor.execute(
        """
        DELETE FROM funcionario
        WHERE id = %s;
        """,
        (funcionario_id,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()


# ============================================================
# SERVIÇOS
# ============================================================

def buscar_servicos_filtrados(
    empresa_id=None,
    mes=None,
    ano=None
):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    consulta = """
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
    """

    condicoes = []
    parametros = []

    if empresa_id is not None:
        condicoes.append("s.empresa_id = %s")
        parametros.append(empresa_id)

    if mes is not None:
        condicoes.append("EXTRACT(MONTH FROM s.data) = %s")
        parametros.append(mes)

    if ano is not None:
        condicoes.append("EXTRACT(YEAR FROM s.data) = %s")
        parametros.append(ano)

    if condicoes:
        consulta += " WHERE " + " AND ".join(condicoes)

    consulta += """
        GROUP BY
            s.id,
            e.nome,
            m.nome,
            s.data,
            s.km,
            s.valor_km_motorista

        ORDER BY s.id ASC;
    """

    cursor.execute(
        consulta,
        parametros
    )

    servicos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return servicos


def buscar_anos_servicos():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT DISTINCT
            EXTRACT(YEAR FROM data)::INTEGER AS ano
        FROM servico
        ORDER BY ano DESC;
    """)

    anos = [
        resultado[0]
        for resultado in cursor.fetchall()
    ]

    cursor.close()
    conexao.close()

    return anos


def buscar_servico_por_id(servico_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            id,
            empresa_id,
            motorista_id,
            data,
            km,
            valor_km_motorista
        FROM servico
        WHERE id = %s;
        """,
        (servico_id,)
    )

    servico = cursor.fetchone()

    cursor.close()
    conexao.close()

    return servico


def buscar_funcionarios_do_servico(servico_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            funcionario_id
        FROM servico_funcionario
        WHERE servico_id = %s
        ORDER BY funcionario_id;
        """,
        (servico_id,)
    )

    funcionarios = [
        resultado[0]
        for resultado in cursor.fetchall()
    ]

    cursor.close()
    conexao.close()

    return funcionarios


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

        raise ValueError(
            "Motorista não encontrado."
        )

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
        RETURNING id, km;
        """,
        (
            empresa_id,
            motorista_id,
            data,
            km,
            valor_km_motorista
        )
    )

    resultado_servico = cursor.fetchone()

    print(
    "SERVIÇO INSERIDO:",
    resultado_servico
    )

    servico_id = resultado_servico[0]

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


def atualizar_servico(
    servico_id,
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

        raise ValueError(
            "Motorista não encontrado."
        )

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
        UPDATE servico
        SET
            empresa_id = %s,
            motorista_id = %s,
            data = %s,
            km = %s,
            valor_km_motorista = %s
        WHERE id = %s;
        """,
        (
            empresa_id,
            motorista_id,
            data,
            km,
            valor_km_motorista,
            servico_id
        )
    )

    cursor.execute(
        """
        DELETE FROM servico_funcionario
        WHERE servico_id = %s;
        """,
        (servico_id,)
    )

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



# ============================================================
# RELATÓRIOS
# ============================================================

def buscar_resumo_relatorio(empresa_id, mes, ano):

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*) AS quantidade_servicos,

            COALESCE(
                SUM(s.km),
                0
            ) AS km_total,

            COALESCE(
                SUM(
                    (
                        SELECT COUNT(*)
                        FROM servico_funcionario sf
                        WHERE sf.servico_id = s.id
                    )
                ),
                0
            ) AS funcionarios_transportados,

            COALESCE(
                SUM(
                    s.km * s.valor_km_motorista
                ),
                0
            ) AS valor_total_motoristas

        FROM servico s

        WHERE s.empresa_id = %s
        AND EXTRACT(MONTH FROM s.data) = %s
        AND EXTRACT(YEAR FROM s.data) = %s;
        """,
        (
            empresa_id,
            mes,
            ano
        )
    )

    resumo = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resumo


def buscar_resumo_motoristas_relatorio(empresa_id, mes, ano):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            m.nome,
            COUNT(DISTINCT s.id) AS quantidade_servicos,
            COALESCE(SUM(s.km), 0) AS km_total,
            COALESCE(
                SUM(s.km * s.valor_km_motorista),
                0
            ) AS valor_total
        FROM servico s
        JOIN motorista m
            ON s.motorista_id = m.id
        WHERE s.empresa_id = %s
        AND EXTRACT(MONTH FROM s.data) = %s
        AND EXTRACT(YEAR FROM s.data) = %s
        GROUP BY
            m.id,
            m.nome
        ORDER BY
            m.nome;
        """,
        (
            empresa_id,
            mes,
            ano
        )
    )

    motoristas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return motoristas

def excluir_servico(servico_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        DELETE FROM servico
        WHERE id = %s;
        """,
        (servico_id,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()