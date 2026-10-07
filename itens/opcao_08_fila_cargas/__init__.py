"""Opcao 8 do menu: fila cargas."""

from interface.entrada import ler_float

def executar(sistema):
    """Executa a opcao 8 usando a instancia principal do sistema."""
    destino = input("Destino (ex.: CEASA): ")
    peso = ler_float("Peso da carga (kg): ")
    frete = ler_float("Valor do frete: R$ ")
    placa = input("Placa do caminhão (opcional): ")
    sistema.adicionar_carga(destino, peso, frete, placa)
    print("Carga entrou na fila.")
