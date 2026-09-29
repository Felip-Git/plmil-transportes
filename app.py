from datetime import datetime

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    redirect,
    url_for,
    send_file
)

from relatorio_excel import (
    gerar_relatorio_excel,
    gerar_relatorio_motoristas_excel
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
    buscar_servicos_por_mes,
    buscar_servico_por_id,
    buscar_funcionarios_do_servico,
    inserir_servico,
    atualizar_servico,
    excluir_servico,
    buscar_resumo_relatorio,
    buscar_resumo_motoristas_relatorio
)


app = Flask(__name__)


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/")
def home():

    return redirect(
        url_for("dashboard")
    )


@app.route("/dashboard")
def dashboard():

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM servico;"
    )

    total_servicos = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM empresa;"
    )

    total_empresas = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM motorista;"
    )

    total_motoristas = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM funcionario;"
    )

    total_funcionarios = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COALESCE(SUM(km), 0)
        FROM servico;
        """
    )

    total_km = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM servico_funcionario;
        """
    )

    total_funcionarios_transportados = (
        cursor.fetchone()[0]
    )

    cursor.execute(
        """
        SELECT data
        FROM servico
        ORDER BY data DESC, id DESC
        LIMIT 1;
        """
    )

    ultimo_servico = cursor.fetchone()

    cursor.close()
    conexao.close()

    # ========================================================
    # SERVIÇOS POR MÊS
    # ========================================================

    ano_atual = datetime.now().year

    servicos_por_mes = buscar_servicos_por_mes(
        ano_atual
    )

    # ========================================================
    # SERVIÇOS RECENTES
    # ========================================================

    todos_servicos = buscar_servicos_filtrados()

    servicos_recentes = todos_servicos[-5:]

    servicos_recentes.reverse()

    return render_template(
        "dashboard.html",
        total_servicos=total_servicos,
        total_empresas=total_empresas,
        total_motoristas=total_motoristas,
        total_funcionarios=total_funcionarios,
        total_km=total_km,
        total_funcionarios_transportados=(
            total_funcionarios_transportados
        ),
        ultimo_servico=ultimo_servico,
        servicos_recentes=servicos_recentes,
        servicos_por_mes=servicos_por_mes,
        ano_atual=ano_atual
    )


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


@app.route(
    "/empresas/cadastrar",
    methods=["GET", "POST"]
)
def cadastrar_empresa():

    if request.method == "POST":

        nome = request.form["nome"]

        inserir_empresa(
            nome
        )

        return redirect(
            url_for("empresas")
        )

    return render_template(
        "cadastrar_empresa.html"
    )


@app.route(
    "/empresas/<int:empresa_id>/editar",
    methods=["GET", "POST"]
)
def editar_empresa(empresa_id):

    empresa = buscar_empresa_por_id(
        empresa_id
    )

    if empresa is None:

        return "Empresa não encontrada.", 404

    if request.method == "POST":

        nome = request.form["nome"]

        atualizar_empresa(
            empresa_id,
            nome
        )

        return redirect(
            url_for("empresas")
        )

    return render_template(
        "editar_empresa.html",
        empresa=empresa
    )


@app.route(
    "/empresas/<int:empresa_id>/excluir",
    methods=["POST"]
)
def excluir_empresa_rota(empresa_id):

    empresa = buscar_empresa_por_id(
        empresa_id
    )

    if empresa is None:

        return "Empresa não encontrada.", 404

    try:

        excluir_empresa(
            empresa_id
        )

    except ValueError as erro:

        return render_template(
            "erro.html",
            mensagem=str(erro),
            voltar=url_for("empresas")
        )

    return redirect(
        url_for("empresas")
    )


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


@app.route(
    "/motoristas/cadastrar",
    methods=["GET", "POST"]
)
def cadastrar_motorista():

    if request.method == "POST":

        nome = request.form["nome"]

        valor_km = request.form[
            "valor_km"
        ].replace(
            ",",
            "."
        )

        inserir_motorista(
            nome,
            valor_km
        )

        return redirect(
            url_for("motoristas")
        )

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

        valor_km = request.form[
            "valor_km"
        ].replace(
            ",",
            "."
        )

        atualizar_motorista(
            motorista_id,
            nome,
            valor_km
        )

        return redirect(
            url_for("motoristas")
        )

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

        excluir_motorista(
            motorista_id
        )

    except ValueError as erro:

        return render_template(
            "erro.html",
            mensagem=str(erro),
            voltar=url_for("motoristas")
        )

    return redirect(
        url_for("motoristas")
    )


# ============================================================
# FUNCIONÁRIOS
# ============================================================

@app.route("/funcionarios")
def funcionarios():

    empresa_id = request.args.get(
        "empresa_id"
    ) or None

    if empresa_id and empresa_id.isdigit():

        empresa_id = int(
            empresa_id
        )

    else:

        empresa_id = None

    if empresa_id is not None:

        lista_funcionarios = (
            buscar_funcionarios_por_empresa(
                empresa_id
            )
        )

    else:

        lista_funcionarios = (
            buscar_funcionarios()
        )

    lista_empresas = buscar_empresas()

    return render_template(
        "funcionarios.html",
        funcionarios=lista_funcionarios,
        empresas=lista_empresas,
        empresa_selecionada=empresa_id
    )


@app.route(
    "/funcionarios/cadastrar",
    methods=["GET", "POST"]
)
def cadastrar_funcionario():

    if request.method == "POST":

        nome = request.form[
            "nome"
        ]

        empresa_id = request.form[
            "empresa_id"
        ]

        inserir_funcionario(
            nome,
            empresa_id
        )

        return redirect(
            url_for("funcionarios")
        )

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

        nome = request.form[
            "nome"
        ]

        empresa_id = request.form[
            "empresa_id"
        ]

        atualizar_funcionario(
            funcionario_id,
            nome,
            empresa_id
        )

        return redirect(
            url_for("funcionarios")
        )

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

        excluir_funcionario(
            funcionario_id
        )

    except ValueError as erro:

        return render_template(
            "erro.html",
            mensagem=str(erro),
            voltar=url_for("funcionarios")
        )

    return redirect(
        url_for("funcionarios")
    )


# ============================================================
# API DE FUNCIONÁRIOS POR EMPRESA
# ============================================================

@app.route(
    "/api/funcionarios/<int:empresa_id>"
)
def api_funcionarios_por_empresa(empresa_id):

    lista_funcionarios = (
        buscar_funcionarios_por_empresa(
            empresa_id
        )
    )

    funcionarios = [
        {
            "id": funcionario[0],
            "nome": funcionario[1]
        }
        for funcionario in lista_funcionarios
    ]

    return jsonify(
        funcionarios
    )


# ============================================================
# ROTA ANTIGA DE FUNCIONÁRIOS POR EMPRESA
# ============================================================

@app.route(
    "/funcionarios/empresa/<int:empresa_id>"
)
def funcionarios_por_empresa(empresa_id):

    lista_funcionarios = (
        buscar_funcionarios_por_empresa(
            empresa_id
        )
    )

    funcionarios = [
        {
            "id": funcionario[0],
            "nome": funcionario[1]
        }
        for funcionario in lista_funcionarios
    ]

    return jsonify(
        funcionarios
    )


# ============================================================
# RELATÓRIO DE EMPRESAS
# ============================================================

@app.route("/relatorios")
def relatorios():

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

        empresa_id = int(
            empresa_id
        )

    else:

        empresa_id = None

    if (
        mes
        and mes.isdigit()
        and 1 <= int(mes) <= 12
    ):

        mes = int(
            mes
        )

    else:

        mes = None

    if ano and ano.isdigit():

        ano = int(
            ano
        )

    else:

        ano = None

    lista_empresas = buscar_empresas()

    anos = buscar_anos_servicos()

    ano_atual = datetime.now().year

    if ano_atual not in anos:

        anos.append(
            ano_atual
        )

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

    servicos = []

    resumo = None

    empresa_selecionada_nome = None

    if empresa_id and mes and ano:

        servicos = buscar_servicos_filtrados(
            empresa_id=empresa_id,
            mes=mes,
            ano=ano
        )

        resumo = buscar_resumo_relatorio(
            empresa_id,
            mes,
            ano
        )

        for empresa in lista_empresas:

            if empresa[0] == empresa_id:

                empresa_selecionada_nome = (
                    empresa[1]
                )

                break

    return render_template(
        "relatorios.html",
        servicos=servicos,
        resumo=resumo,
        empresas=lista_empresas,
        anos=anos,
        meses=meses,
        empresa_selecionada=empresa_id,
        mes_selecionado=mes,
        ano_selecionado=ano,
        empresa_selecionada_nome=(
            empresa_selecionada_nome
        )
    )


# ============================================================
# RELATÓRIO DE MOTORISTAS
# ============================================================

@app.route("/relatorios/motoristas")
def relatorios_motoristas():

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

        empresa_id = int(
            empresa_id
        )

    else:

        empresa_id = None

    if (
        mes
        and mes.isdigit()
        and 1 <= int(mes) <= 12
    ):

        mes = int(
            mes
        )

    else:

        mes = None

    if ano and ano.isdigit():

        ano = int(
            ano
        )

    else:

        ano = None

    lista_empresas = buscar_empresas()

    anos = buscar_anos_servicos()

    ano_atual = datetime.now().year

    if ano_atual not in anos:

        anos.append(
            ano_atual
        )

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

    resumo_motoristas = []

    resumo_quantidade_servicos = 0

    resumo_km_total = 0

    resumo_valor_total = 0

    empresa_selecionada_nome = None

    if empresa_id and mes and ano:

        resumo_motoristas = (
            buscar_resumo_motoristas_relatorio(
                empresa_id,
                mes,
                ano
            )
        )

        resumo_quantidade_servicos = sum(
            motorista[1]
            for motorista in resumo_motoristas
        )

        resumo_km_total = sum(
            float(motorista[2])
            for motorista in resumo_motoristas
        )

        resumo_valor_total = sum(
            float(motorista[3])
            for motorista in resumo_motoristas
        )

        for empresa in lista_empresas:

            if empresa[0] == empresa_id:

                empresa_selecionada_nome = (
                    empresa[1]
                )

                break

    return render_template(
        "relatorios_motoristas.html",
        resumo_motoristas=resumo_motoristas,
        resumo_quantidade_servicos=(
            resumo_quantidade_servicos
        ),
        resumo_km_total=(
            resumo_km_total
        ),
        resumo_valor_total=(
            resumo_valor_total
        ),
        empresas=lista_empresas,
        anos=anos,
        meses=meses,
        empresa_selecionada=empresa_id,
        mes_selecionado=mes,
        ano_selecionado=ano,
        empresa_selecionada_nome=(
            empresa_selecionada_nome
        )
    )


# ============================================================
# EXPORTAÇÃO DO RELATÓRIO DE EMPRESAS
# ============================================================

@app.route(
    "/relatorios/exportar"
)
def exportar_relatorio():

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

        empresa_id = int(
            empresa_id
        )

    else:

        empresa_id = None

    if (
        mes
        and mes.isdigit()
        and 1 <= int(mes) <= 12
    ):

        mes = int(
            mes
        )

    else:

        mes = None

    if ano and ano.isdigit():

        ano = int(
            ano
        )

    else:

        ano = None

    if not empresa_id or not mes or not ano:

        return (
            "Selecione empresa, mês e ano "
            "para exportar o relatório.",
            400
        )

    lista_empresas = buscar_empresas()

    empresa_selecionada_nome = None

    for empresa in lista_empresas:

        if empresa[0] == empresa_id:

            empresa_selecionada_nome = (
                empresa[1]
            )

            break

    if empresa_selecionada_nome is None:

        return (
            "Empresa não encontrada.",
            404
        )

    servicos = buscar_servicos_filtrados(
        empresa_id=empresa_id,
        mes=mes,
        ano=ano
    )

    resumo = buscar_resumo_relatorio(
        empresa_id,
        mes,
        ano
    )

    arquivo = gerar_relatorio_excel(
        empresa_nome=empresa_selecionada_nome,
        mes=mes,
        ano=ano,
        resumo=resumo,
        servicos=servicos
    )

    nome_arquivo = (
        f"relatorio_"
        f"{empresa_selecionada_nome}"
        f"_{mes:02d}"
        f"_{ano}.xlsx"
    )

    return send_file(
        arquivo,
        as_attachment=True,
        download_name=nome_arquivo,
        mimetype=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )


# ============================================================
# EXPORTAÇÃO DO RELATÓRIO DE MOTORISTAS
# ============================================================

@app.route(
    "/relatorios/motoristas/exportar"
)
def exportar_relatorio_motoristas():

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

        empresa_id = int(
            empresa_id
        )

    else:

        empresa_id = None

    if (
        mes
        and mes.isdigit()
        and 1 <= int(mes) <= 12
    ):

        mes = int(
            mes
        )

    else:

        mes = None

    if ano and ano.isdigit():

        ano = int(
            ano
        )

    else:

        ano = None

    if not empresa_id or not mes or not ano:

        return (
            "Selecione empresa, mês e ano "
            "para exportar o relatório.",
            400
        )

    lista_empresas = buscar_empresas()

    empresa_selecionada_nome = None

    for empresa in lista_empresas:

        if empresa[0] == empresa_id:

            empresa_selecionada_nome = (
                empresa[1]
            )

            break

    if empresa_selecionada_nome is None:

        return (
            "Empresa não encontrada.",
            404
        )

    resumo = buscar_resumo_relatorio(
        empresa_id,
        mes,
        ano
    )

    resumo_motoristas = (
        buscar_resumo_motoristas_relatorio(
            empresa_id,
            mes,
            ano
        )
    )

    arquivo = gerar_relatorio_motoristas_excel(
        empresa_nome=empresa_selecionada_nome,
        mes=mes,
        ano=ano,
        resumo=resumo,
        resumo_motoristas=resumo_motoristas
    )

    nome_arquivo = (
        f"relatorio_motoristas_"
        f"{empresa_selecionada_nome}"
        f"_{mes:02d}"
        f"_{ano}.xlsx"
    )

    return send_file(
        arquivo,
        as_attachment=True,
        download_name=nome_arquivo,
        mimetype=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )


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

        empresa_id = int(
            empresa_id
        )

    else:

        empresa_id = None

    if (
        mes
        and mes.isdigit()
        and 1 <= int(mes) <= 12
    ):

        mes = int(
            mes
        )

    else:

        mes = None

    if ano and ano.isdigit():

        ano = int(
            ano
        )

    else:

        ano = None

    lista_servicos = (
        buscar_servicos_filtrados(
            empresa_id=empresa_id,
            mes=mes,
            ano=ano
        )
    )

    lista_empresas = buscar_empresas()

    anos = buscar_anos_servicos()

    ano_atual = datetime.now().year

    if ano_atual not in anos:

        anos.append(
            ano_atual
        )

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


# ============================================================
# DETALHES DO SERVIÇO
# ============================================================

@app.route(
    "/servicos/<int:servico_id>"
)
def detalhes_servico(servico_id):

    servico = buscar_servico_por_id(
        servico_id
    )

    if servico is None:

        return "Serviço não encontrado.", 404

    lista_empresas = buscar_empresas()

    empresa_nome = "Empresa não encontrada"

    for empresa in lista_empresas:

        if empresa[0] == servico[1]:

            empresa_nome = empresa[1]

            break

    lista_motoristas = buscar_motoristas()

    motorista_nome = "Motorista não encontrado"

    for motorista in lista_motoristas:

        if motorista[0] == servico[2]:

            motorista_nome = motorista[1]

            break

    funcionarios_ids = (
        buscar_funcionarios_do_servico(
            servico_id
        )
    )

    funcionarios = []

    for funcionario_id in funcionarios_ids:

        funcionario = buscar_funcionario_por_id(
            funcionario_id
        )

        if funcionario is not None:

            funcionarios.append(
                funcionario
            )

    valor_motorista = (
        float(servico[4])
        *
        float(servico[5])
    )

    return render_template(
        "detalhes_servico.html",
        servico=servico,
        empresa_nome=empresa_nome,
        motorista_nome=motorista_nome,
        funcionarios=funcionarios,
        valor_motorista=valor_motorista
    )


# ============================================================
# CADASTRAR SERVIÇO
# ============================================================

@app.route(
    "/servicos/cadastrar",
    methods=["GET", "POST"]
)
def cadastrar_servico():

    if request.method == "POST":

        empresa_id = request.form[
            "empresa_id"
        ]

        motorista_id = request.form[
            "motorista_id"
        ]

        data = request.form[
            "data"
        ]

        km = request.form[
            "km"
        ]

        funcionarios_ids = (
            request.form.getlist(
                "funcionarios_ids"
            )
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


# ============================================================
# EDITAR SERVIÇO
# ============================================================

@app.route(
    "/servicos/<int:servico_id>/editar",
    methods=["GET", "POST"]
)
def editar_servico(servico_id):

    servico = buscar_servico_por_id(
        servico_id
    )

    if servico is None:

        return (
            "Serviço não encontrado.",
            404
        )

    # ========================================================
    # SALVAR ALTERAÇÕES
    # ========================================================

    if request.method == "POST":

        empresa_id = request.form[
            "empresa_id"
        ]

        motorista_id = request.form[
            "motorista_id"
        ]

        data = request.form[
            "data"
        ]

        km = request.form[
            "km"
        ]

        # O editar_servico.html utiliza "funcionarios".
        # Mantemos também "funcionarios_ids" como
        # compatibilidade com outras telas.

        funcionarios_ids = (
            request.form.getlist(
                "funcionarios"
            )
        )

        if not funcionarios_ids:

            funcionarios_ids = (
                request.form.getlist(
                    "funcionarios_ids"
                )
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

    # ========================================================
    # CARREGAR DADOS DA TELA
    # ========================================================

    lista_empresas = buscar_empresas()

    lista_motoristas = buscar_motoristas()

    funcionarios_ids = (
        buscar_funcionarios_do_servico(
            servico_id
        )
    )

    funcionarios_selecionados = []

    for funcionario_id in funcionarios_ids:

        funcionario = buscar_funcionario_por_id(
            funcionario_id
        )

        if funcionario is not None:

            funcionarios_selecionados.append(
                {
                    "id": funcionario[0],
                    "nome": funcionario[1]
                }
            )

    return render_template(
        "editar_servico.html",
        servico=servico,
        empresas=lista_empresas,
        motoristas=lista_motoristas,
        funcionarios_selecionados=(
            funcionarios_selecionados
        )
    )


# ============================================================
# EXCLUIR SERVIÇO
# ============================================================

@app.route(
    "/servicos/<int:servico_id>/excluir",
    methods=["POST"]
)
def excluir_servico_rota(servico_id):

    servico = buscar_servico_por_id(
        servico_id
    )

    if servico is None:

        return (
            "Serviço não encontrado.",
            404
        )

    excluir_servico(
        servico_id
    )

    return redirect(
        url_for("servicos")
    )


# ============================================================
# CONFIGURAÇÕES
# ============================================================

@app.route("/configuracoes")
def configuracoes():

    conexao = None

    banco_conectado = False

    try:

        conexao = conectar_banco()

        if conexao:

            banco_conectado = True

    except Exception:

        banco_conectado = False

    finally:

        if conexao:

            conexao.close()

    configuracoes_sistema = {

        "nome": "PL Mil Transportes",

        "descricao": "Gestão de transportes",

        "versao": "1.0.0",

        "data": "DD/MM/AAAA",

        "moeda": "Real brasileiro (R$)",

        "idioma": "Português (Brasil)",

        "backend": "Python + Flask",

        "banco": "PostgreSQL",

        "interface": "HTML + CSS + JavaScript"

    }

    return render_template(
        "configuracoes.html",
        banco_conectado=banco_conectado,
        configuracoes_sistema=configuracoes_sistema
    )


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )

