from flask import Flask, render_template, request, redirect, url_for

from database import (
    conectar_banco,
    buscar_empresas,
    inserir_empresa,
    buscar_motoristas,
    inserir_motorista,
    buscar_funcionarios,
    inserir_funcionario,
    buscar_pedidos,
    inserir_pedido
)


app = Flask(__name__)


@app.route("/")
def home():
    conexao = conectar_banco()
    conexao.close()

    return "Flask conectado ao PostgreSQL!"


@app.route("/empresas")
def empresas():
    lista_empresas = buscar_empresas()

    return render_template(
        "empresas.html",
        empresas=lista_empresas
    )


@app.route("/empresas/cadastrar", methods=["GET", "POST"])
def cadastrar_empresa():

    if request.method == "POST":
        nome = request.form["nome"]

        inserir_empresa(nome)

        return redirect(url_for("empresas"))

    return render_template("cadastrar_empresa.html")


@app.route("/motoristas")
def motoristas():
    lista_motoristas = buscar_motoristas()

    return render_template(
        "motoristas.html",
        motoristas=lista_motoristas
    )


@app.route("/motoristas/cadastrar", methods=["GET", "POST"])
def cadastrar_motorista():

    if request.method == "POST":
        nome = request.form["nome"]

        inserir_motorista(nome)

        return redirect(url_for("motoristas"))

    return render_template("cadastrar_motorista.html")


@app.route("/funcionarios")
def funcionarios():
    lista_funcionarios = buscar_funcionarios()

    return render_template(
        "funcionarios.html",
        funcionarios=lista_funcionarios
    )


@app.route("/funcionarios/cadastrar", methods=["GET", "POST"])
def cadastrar_funcionario():

    if request.method == "POST":
        nome = request.form["nome"]

        inserir_funcionario(nome)

        return redirect(url_for("funcionarios"))

    return render_template("cadastrar_funcionario.html")


@app.route("/pedidos")
def pedidos():
    lista_pedidos = buscar_pedidos()

    return render_template(
        "pedidos.html",
        pedidos=lista_pedidos
    )


@app.route("/pedidos/cadastrar", methods=["GET", "POST"])
def cadastrar_pedido():

    if request.method == "POST":
        empresa_id = request.form["empresa_id"]

        inserir_pedido(empresa_id)

        return redirect(url_for("pedidos"))

    lista_empresas = buscar_empresas()

    return render_template(
        "cadastrar_pedido.html",
        empresas=lista_empresas
    )


if __name__ == "__main__":
    app.run(debug=True)