
<!-- BANNER -->
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0D47A1,50:1565C0,100:42A5F5&height=180&section=header&text=PL%20Mil%20Transportes&fontSize=36&fontColor=FFFFFF&fontAlignY=38" width="100%" />
</p>

<h1 align="center">Sistema de Gestão de Transportes</h1>

<p align="center">
  Aplicação web para organizar serviços de transporte de funcionários,
  centralizar informações operacionais e facilitar o acompanhamento dos serviços.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-0D47A1?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-1565C0?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-1976D2?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Excel-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white" />
</p>

---

## 📌 Sobre o projeto

O **PL Mil Transportes** é uma aplicação web desenvolvida para auxiliar no gerenciamento dos serviços de transporte de funcionários realizados pela empresa.

O projeto surgiu a partir de uma necessidade real: melhorar o controle das informações relacionadas aos serviços, que envolvem empresas contratantes, motoristas, funcionários transportados, datas, quilometragem e valores pagos.

A proposta foi desenvolver uma solução que centralizasse esses dados em um único sistema, reduzindo controles manuais e facilitando a consulta e a geração de relatórios.

## 🎯 Objetivo

Desenvolver uma ferramenta para organizar as operações de transporte, facilitar o registro dos serviços e disponibilizar informações que auxiliem no acompanhamento das atividades e no controle financeiro.

## ⚙️ Funcionalidades

### Cadastro e gerenciamento

- Cadastro, edição e exclusão de empresas.
- Cadastro, edição e exclusão de motoristas.
- Cadastro e gerenciamento de funcionários vinculados às empresas.
- Associação de funcionários aos respectivos serviços.

### Controle de serviços

- Registro de serviços de transporte.
- Seleção da empresa e do motorista responsável.
- Registro da data e da quilometragem percorrida.
- Seleção dos funcionários transportados.
- Edição e exclusão de serviços.

### Cálculos automáticos

- Consulta do valor por quilômetro cadastrado para cada motorista.
- Cálculo automático do valor a pagar ao motorista com base na quilometragem.
- Armazenamento do valor por quilômetro aplicado ao serviço.

### Dashboard e relatórios

- Dashboard com indicadores gerais da operação.
- Visualização da quantidade de serviços, empresas, motoristas e funcionários.
- Acompanhamento da quilometragem total.
- Visualização de serviços por mês.
- Filtros de relatórios por empresa, mês e ano.
- Resumo dos serviços e dos valores pagos aos motoristas.
- Exportação de relatórios para Excel.

### Controle de acesso

- Tela de autenticação.
- Cadastro e gerenciamento de usuários.
- Perfis de acesso de administrador e operador.
- Ativação e desativação de usuários.
- Armazenamento de senhas com hash.

---

## 🧰 Tecnologias utilizadas

| Tecnologia | Aplicação no projeto |
|---|---|
| Python | Linguagem principal |
| Flask | Desenvolvimento da aplicação web |
| PostgreSQL | Banco de dados relacional |
| psycopg2 | Comunicação com o PostgreSQL |
| HTML e CSS | Estrutura e apresentação das páginas |
| JavaScript | Interações da interface |
| OpenPyXL | Geração de relatórios Excel |
| Gunicorn | Servidor de aplicação para implantação |
| Git e GitHub | Versionamento do projeto |
| Render | Hospedagem da aplicação |

---

## 🗂️ Estrutura do projeto

```text
plmil-transportes/
│
├── app.py
├── database.py
├── relatorio_excel.py
├── requirements.txt
├── .gitignore
│
├── templates/
│   ├── dashboard.html
│   ├── login.html
│   ├── empresas.html
│   ├── motoristas.html
│   ├── funcionarios.html
│   ├── servicos.html
│   ├── relatorios.html
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   └── ...
│
└── README.md
```

---

## 🚀 Como executar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/Felip-Git/plmil-transportes.git
```

### 2. Entre na pasta do projeto

```bash
cd plmil-transportes
```

### 3. Crie um ambiente virtual

```bash
python -m venv venv
```

Ative o ambiente virtual no Windows:

```bash
venv\Scripts\activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
FLASK_SECRET_KEY=sua_chave_secreta

DB_HOST=localhost
DB_PORT=5432
DB_NAME=nome_do_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
```

Também é possível utilizar `DATABASE_URL` para conectar a aplicação a uma instância PostgreSQL que forneça uma URL de conexão.

**Importante:** o arquivo `.env` contém informações sensíveis e não deve ser enviado ao GitHub.

### 6. Configure o banco de dados

Crie um banco de dados PostgreSQL e prepare as tabelas necessárias para a aplicação antes de executá-la.

### 7. Execute a aplicação

```bash
flask --app app run --debug
```

Acesse no navegador:

```text
http://127.0.0.1:5000
```

---

## 📊 Aprendizados e aplicações práticas

O desenvolvimento deste projeto permitiu trabalhar com conceitos importantes de desenvolvimento de sistemas e organização de dados:

- Integração entre Python e PostgreSQL.
- Modelagem e manipulação de dados relacionais.
- Desenvolvimento de aplicações web com Flask.
- Implementação de operações CRUD.
- Relacionamento entre diferentes entidades do sistema.
- Cálculos automatizados a partir de dados cadastrados.
- Autenticação e controle de acesso.
- Geração de relatórios e exportação de dados para Excel.
- Implantação de uma aplicação web.

## 🔮 Possíveis evoluções

O projeto pode continuar evoluindo com novas funcionalidades, melhorias de usabilidade e recursos de análise para ampliar o acompanhamento operacional e financeiro.

---

## 👨‍💻 Desenvolvedor

**Felipe Martins**

Estudante de Análise e Desenvolvimento de Sistemas no IFSul, com interesse em desenvolvimento de sistemas, análise de dados e automação de processos.

<p align="left">
  <a href="https://www.linkedin.com/in/felipe-martins-b62714237/">
    <img src="https://img.shields.io/badge/LinkedIn-0D47A1?style=for-the-badge&logo=linkedin&logoColor=white" />
  </a>
  <a href="https://github.com/Felip-Git">
    <img src="https://img.shields.io/badge/GitHub-1565C0?style=for-the-badge&logo=github&logoColor=white" />
  </a>
</p>

<p align="center">
  Desenvolvido com Python, organização e foco em resolver problemas reais.
</p>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:42A5F5,50:1565C0,100:0D47A1&height=100&section=footer" width="100%" />
</p>
