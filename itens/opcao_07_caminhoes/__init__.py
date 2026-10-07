"""Opcao 7 do menu: caminhoes."""

from interface.entrada import ler_float

def executar(sistema):
    """Executa a opcao 7 usando a instancia principal do sistema."""
    placa = input("Placa: ")
    modelo = input("Modelo: ")
    capacidade = ler_float("Capacidade em kg: ")
    custo_km = ler_float("Custo por km: R$ ")
    motorista = input("Motorista: ")
    sistema.cadastrar_caminhao(
        placa, modelo, capacidade, custo_km, motorista
    )
    print("Caminhão cadastrado.")
