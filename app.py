from datetime import datetime

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    redirect,
    url_for
)

from database import (
    conectar_banco,
    buscar_empresas,
    inserir_empresa,
    buscar_motoristas,
    inserir_motorista,
    buscar_funcionarios,
    buscar_funcionarios_por_empresa,
    inserir_funcionario,
    buscar_servicos,
    inserir_servico
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

        valor_km = request.form["valor_km"].replace(",", ".")

        inserir_motorista(
            nome,
            valor_km
        )

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

        empresa_id = request.form["empresa_id"]

        inserir_funcionario(
            nome,
            empresa_id
        )

        return redirect(url_for("funcionarios"))

    lista_empresas = buscar_empresas()

    return render_template(
        "cadastrar_funcionario.html",
        empresas=lista_empresas
    )


@app.route("/funcionarios/empresa/<int:empresa_id>")
def funcionarios_por_empresa(empresa_id):

    lista_funcionarios = buscar_funcionarios_por_empresa(
        empresa_id
    )

    funcionarios = [
        {
            "id": funcionario[0],
            "nome": funcionario[1]
        }
        for funcionario in lista_funcionarios
    ]

    return jsonify(funcionarios)


@app.route("/servicos")
def servicos():
    lista_servicos = buscar_servicos()

    return render_template(
        "servicos.html",
        servicos=lista_servicos
    )


@app.route("/servicos/cadastrar", methods=["GET", "POST"])
def cadastrar_servico():

    if request.method == "POST":

        empresa_id = request.form["empresa_id"]

        motorista_id = request.form["motorista_id"]

        data = request.form["data"]

        km = request.form["km"]

        funcionarios_ids = request.form.getlist(
            "funcionarios_ids"
        )

        data = datetime.strptime(
            data,
            "%Y-%m-%d"
        ).date()

        inserir_servico(
            empresa_id,
            motorista_id,
            data,
            km,
            funcionarios_ids
        )

        return redirect(url_for("servicos"))

    lista_empresas = buscar_empresas()

    lista_motoristas = buscar_motoristas()

    return render_template(
        "cadastrar_servico.html",
        empresas=lista_empresas,
        motoristas=lista_motoristas
    )


if __name__ == "__main__":
    app.run(debug=True) 