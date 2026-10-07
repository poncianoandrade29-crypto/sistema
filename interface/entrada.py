"""Console input and number validation."""

import math


def ler_float(msg):
    """Lê um número decimal finito, aceitando vírgula como separador."""
    while True:
        try:
            valor = float(input(msg).replace(",", "."))
            if not math.isfinite(valor):
                raise ValueError
            return valor
        except ValueError:
            print("Digite um número válido.")

def ler_int(msg):
    """Lê um número inteiro, repetindo a pergunta enquanto for inválido."""
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Digite um número inteiro válido.")
