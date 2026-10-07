"""Opcao 14 do menu: cadastro tarefas."""

from interface.entrada import ler_int

def executar(sistema):
    """Executa a opcao 14 usando a instancia principal do sistema."""
    prioridade = ler_int(
        "Prioridade (1=urgente, 5=baixa): "
    )
    descricao = input("Tarefa: ")
    sistema.adicionar_tarefa(prioridade, descricao)
    print("Tarefa adicionada.")
