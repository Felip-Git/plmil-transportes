import os

import psycopg2
from dotenv import load_dotenv


load_dotenv()


def conectar_banco():
    conexao = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    return conexao


def buscar_empresas():
    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM empresa;")

    empresas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return empresas


def inserir_empresa(nome):
    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO empresa (nome) VALUES (%s);",
        (nome,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()


def buscar_motoristas():
    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM motorista;")

    motoristas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return motoristas


def inserir_motorista(nome):
    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO motorista (nome) VALUES (%s);",
        (nome,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()


def buscar_funcionarios():
    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM funcionario;")

    funcionarios = cursor.fetchall()

    cursor.close()
    conexao.close()

    return funcionarios


def inserir_funcionario(nome):
    conexao = conectar_banco()

    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO funcionario (nome) VALUES (%s);",
        (nome,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()