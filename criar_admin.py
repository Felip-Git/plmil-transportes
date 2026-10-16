import getpass

from werkzeug.security import generate_password_hash

from database import inserir_usuario


print("=" * 50)
print("CRIAR USUÁRIO ADMINISTRADOR")
print("=" * 50)


nome = input("Nome: ").strip()

email = input("E-mail: ").strip().lower()

senha = getpass.getpass(
    "Senha: "
)

confirmacao = getpass.getpass(
    "Confirme a senha: "
)


if not nome:
    print("\nErro: o nome não pode ficar vazio.")

    raise SystemExit


if not email:
    print("\nErro: o e-mail não pode ficar vazio.")

    raise SystemExit


if not senha:
    print("\nErro: a senha não pode ficar vazia.")

    raise SystemExit


if senha != confirmacao:

    print("\nErro: as senhas não são iguais.")

    raise SystemExit


senha_hash = generate_password_hash(
    senha
)


try:

    usuario_id = inserir_usuario(
        nome=nome,
        email=email,
        senha_hash=senha_hash,
        perfil="ADMINISTRADOR"
    )

    print("\nUsuário administrador criado com sucesso!")

    print(
        f"ID do usuário: {usuario_id}"
    )

    print(
        f"E-mail: {email}"
    )

except Exception as erro:

    print(
        "\nNão foi possível criar o usuário."
    )

    print(
        f"Erro: {erro}"
    )