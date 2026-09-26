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
    buscar_empresa_por_id,
    inserir_empresa,
    atualizar_empresa,
    excluir_empresa,
    buscar_motoristas,
    buscar_motorista_por_id,
    inserir_motorista,
    atualizar_motorista,
    excluir_motorista,
    buscar_funcionarios,
    buscar_funcionario_por_id,
    buscar_funcionarios_por_empresa,
    inserir_funcionario,
    atualizar_funcionario,
    excluir_funcionario,
    buscar_servicos_filtrados,
    buscar_anos_servicos,
    buscar_servico_por_id,
    buscar_funcionarios_do_servico,
    inserir_servico,
    atualizar_servico,
    excluir_servico
)


app = Flask(__name__)


@app.route("/")
def home():
    conexao = conectar_banco()
    conexao.close()

    return "Flask conectado ao PostgreSQL!"


# ============================================================
# EMPRESAS
# ============================================================

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

    return render_template(
        "cadastrar_empresa.html"
    )


@app.route("/empresas/<int:empresa_id>/editar", methods=["GET", "POST"])
def editar_empresa(empresa_id):

    empresa = buscar_empresa_por_id(empresa_id)

    if empresa is None:
        return "Empresa não encontrada.", 404

    if request.method == "POST":

        nome = request.form["nome"]

        atualizar_empresa(
            empresa_id,
            nome
        )

        return redirect(url_for("empresas"))

    return render_template(
        "editar_empresa.html",
        empresa=empresa
    )


@app.route("/empresas/<int:empresa_id>/excluir", methods=["POST"])
def excluir_empresa_rota(empresa_id):

    empresa = buscar_empresa_por_id(empresa_id)

    if empresa is None:
        return "Empresa não encontrada.", 404

    try:

        excluir_empresa(empresa_id)

    except ValueError as erro:

        return render_template(
            "erro.html",
            mensagem=str(erro),
            voltar=url_for("empresas")
        )

    return redirect(url_for("empresas"))


# ============================================================
# MOTORISTAS
# ============================================================

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

        valor_km = request.form["valor_km"].replace(
            ",",
            "."
        )

        inserir_motorista(
            nome,
            valor_km
        )

        return redirect(url_for("motoristas"))

    return render_template(
        "cadastrar_motorista.html"
    )


@app.route(
    "/motoristas/<int:motorista_id>/editar",
    methods=["GET", "POST"]
)
def editar_motorista(motorista_id):

    motorista = buscar_motorista_por_id(
        motorista_id
    )

    if motorista is None:
        return "Motorista não encontrado.", 404

    if request.method == "POST":

        nome = request.form["nome"]

        valor_km = request.form["valor_km"].replace(
            ",",
            "."
        )

        atualizar_motorista(
            motorista_id,
            nome,
            valor_km
        )

        return redirect(url_for("motoristas"))

    return render_template(
        "editar_motorista.html",
        motorista=motorista
    )


@app.route(
    "/motoristas/<int:motorista_id>/excluir",
    methods=["POST"]
)
def excluir_motorista_rota(motorista_id):

    motorista = buscar_motorista_por_id(
        motorista_id
    )

    if motorista is None:
        return "Motorista não encontrado.", 404

    try:

        excluir_motorista(motorista_id)

    except ValueError as erro:

        return render_template(
            "erro.html",
            mensagem=str(erro),
            voltar=url_for("motoristas")
        )

    return redirect(url_for("motoristas"))


# ============================================================
# FUNCIONÁRIOS
# ============================================================

@app.route("/funcionarios")
def funcionarios():

    lista_funcionarios = buscar_funcionarios()

    return render_template(
        "funcionarios.html",
        funcionarios=lista_funcionarios
    )


@app.route(
    "/funcionarios/cadastrar",
    methods=["GET", "POST"]
)
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


@app.route(
    "/funcionarios/<int:funcionario_id>/editar",
    methods=["GET", "POST"]
)
def editar_funcionario(funcionario_id):

    funcionario = buscar_funcionario_por_id(
        funcionario_id
    )

    if funcionario is None:
        return "Funcionário não encontrado.", 404

    if request.method == "POST":

        nome = request.form["nome"]

        empresa_id = request.form["empresa_id"]

        atualizar_funcionario(
            funcionario_id,
            nome,
            empresa_id
        )

        return redirect(url_for("funcionarios"))

    lista_empresas = buscar_empresas()

    return render_template(
        "editar_funcionario.html",
        funcionario=funcionario,
        empresas=lista_empresas
    )


@app.route(
    "/funcionarios/<int:funcionario_id>/excluir",
    methods=["POST"]
)
def excluir_funcionario_rota(funcionario_id):

    funcionario = buscar_funcionario_por_id(
        funcionario_id
    )

    if funcionario is None:
        return "Funcionário não encontrado.", 404

    try:

        excluir_funcionario(funcionario_id)

    except ValueError as erro:

        return render_template(
            "erro.html",
            mensagem=str(erro),
            voltar=url_for("funcionarios")
        )

    return redirect(url_for("funcionarios"))


@app.route(
    "/funcionarios/empresa/<int:empresa_id>"
)
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


# ============================================================
# SERVIÇOS
# ============================================================

@app.route("/servicos")
def servicos():

    empresa_id = request.args.get(
        "empresa_id"
    ) or None

    mes = request.args.get(
        "mes"
    ) or None

    ano = request.args.get(
        "ano"
    ) or None

    if empresa_id and empresa_id.isdigit():
        empresa_id = int(empresa_id)
    else:
        empresa_id = None

    if mes and mes.isdigit() and 1 <= int(mes) <= 12:
        mes = int(mes)
    else:
        mes = None

    if ano and ano.isdigit():
        ano = int(ano)
    else:
        ano = None

    lista_servicos = buscar_servicos_filtrados(
        empresa_id=empresa_id,
        mes=mes,
        ano=ano
    )

    lista_empresas = buscar_empresas()

    anos = buscar_anos_servicos()

    ano_atual = datetime.now().year

    if ano_atual not in anos:
        anos.append(ano_atual)

    anos = sorted(
        anos,
        reverse=True
    )

    meses = [
        (1, "Janeiro"),
        (2, "Fevereiro"),
        (3, "Março"),
        (4, "Abril"),
        (5, "Maio"),
        (6, "Junho"),
        (7, "Julho"),
        (8, "Agosto"),
        (9, "Setembro"),
        (10, "Outubro"),
        (11, "Novembro"),
        (12, "Dezembro")
    ]

    return render_template(
        "servicos.html",
        servicos=lista_servicos,
        empresas=lista_empresas,
        anos=anos,
        meses=meses,
        empresa_selecionada=empresa_id,
        mes_selecionado=mes,
        ano_selecionado=ano
    )


@app.route(
    "/servicos/cadastrar",
    methods=["GET", "POST"]
)
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

        return redirect(
            url_for("servicos")
        )

    lista_empresas = buscar_empresas()

    lista_motoristas = buscar_motoristas()

    return render_template(
        "cadastrar_servico.html",
        empresas=lista_empresas,
        motoristas=lista_motoristas
    )


@app.route(
    "/servicos/<int:servico_id>/editar",
    methods=["GET", "POST"]
)
def editar_servico(servico_id):

    servico = buscar_servico_por_id(
        servico_id
    )

    if servico is None:
        return "Serviço não encontrado.", 404

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

        atualizar_servico(
            servico_id,
            empresa_id,
            motorista_id,
            data,
            km,
            funcionarios_ids
        )

        return redirect(
            url_for("servicos")
        )

    lista_empresas = buscar_empresas()

    lista_motoristas = buscar_motoristas()

    funcionarios_selecionados = (
        buscar_funcionarios_do_servico(
            servico_id
        )
    )

    return render_template(
        "editar_servico.html",
        servico=servico,
        empresas=lista_empresas,
        motoristas=lista_motoristas,
        funcionarios_selecionados=funcionarios_selecionados
    )


@app.route(
    "/servicos/<int:servico_id>/excluir",
    methods=["POST"]
)
def excluir_servico_rota(servico_id):

    servico = buscar_servico_por_id(
        servico_id
    )

    if servico is None:
        return "Serviço não encontrado.", 404

    excluir_servico(servico_id)

    return redirect(
        url_for("servicos")
    )


if __name__ == "__main__":
    app.run(debug=True)