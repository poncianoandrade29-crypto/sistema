"""Opcao 15 do menu: consulta tarefas."""

def executar(sistema):
    """Executa a opcao 15 usando a instancia principal do sistema."""
    print("\nFila de tarefas:")
    for tarefa in sistema.tarefas.listar():
        print(f"Prioridade {tarefa[0]} - {tarefa[2]}")
    tarefa = sistema.proxima_tarefa()
    print("Próxima:", tarefa if tarefa else "nenhuma")
