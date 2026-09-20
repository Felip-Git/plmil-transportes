from flask import Flask
from database import conectar_banco

app = Flask(__name__)


@app.route("/")
def home():
    conexao = conectar_banco()
    conexao.close()

    return "Flask conectado ao PostgreSQL!"


if __name__ == "__main__":
    app.run(debug=True)