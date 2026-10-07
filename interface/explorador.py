"""File explorer limited to the Sistema Tomate folder."""

import os

PASTA_SISTEMA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def explorar_arquivos():
    """Navega por pastas e arquivos sem sair da pasta do Sistema Tomate."""
    pasta_atual = os.path.realpath(PASTA_SISTEMA)

    while True:
        print(f"\n--- EXPLORADOR DO SISTEMA TOMATE ---\n{pasta_atual}")
        try:
            entradas = sorted(
                os.scandir(pasta_atual),
                key=lambda entrada: (not entrada.is_dir(follow_symlinks=False),
                                     entrada.name.lower()),
            )
        except OSError as erro:
            print(f"Não foi possível listar esta pasta: {erro}")
            return

        pastas = [
            entrada for entrada in entradas
            if entrada.is_dir(follow_symlinks=False)
        ]
        arquivos = [
            entrada for entrada in entradas
            if entrada.is_file(follow_symlinks=False)
        ]

        opcoes_pasta = {}
        proxima_opcao = 1
        for entrada in pastas:
            opcoes_pasta[str(proxima_opcao)] = entrada.path
            print(f"{proxima_opcao} - [Pasta] {entrada.name}")
            proxima_opcao += 1

        for entrada in arquivos:
            try:
                tamanho = entrada.stat(follow_symlinks=False).st_size
                print(f"    {entrada.name} ({tamanho:,} bytes)")
            except OSError as erro:
                print(f"    {entrada.name} (não foi possível ler: {erro})")

        if not pastas and not arquivos:
            print("Esta pasta está vazia.")

        if os.path.realpath(pasta_atual) != os.path.realpath(PASTA_SISTEMA):
            print("0 - Voltar para a pasta anterior")
        print("S - Fechar explorador")

        escolha = input("Escolha uma pasta ou ação: ").strip().lower()
        if escolha == "s":
            return
        if escolha == "0":
            raiz = os.path.realpath(PASTA_SISTEMA)
            atual = os.path.realpath(pasta_atual)
            if atual != raiz:
                pasta_atual = os.path.dirname(atual)
            continue

        destino = opcoes_pasta.get(escolha)
        if destino is None:
            print("Opção inválida.")
            continue

        destino_real = os.path.realpath(destino)
        raiz = os.path.realpath(PASTA_SISTEMA)
        if os.path.commonpath((raiz, destino_real)) != raiz:
            print("A navegação está limitada à pasta do Sistema Tomate.")
            continue
        pasta_atual = destino_real
