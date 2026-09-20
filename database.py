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