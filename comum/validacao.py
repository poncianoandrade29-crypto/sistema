"""Validacao comum para valores numericos do sistema."""

import math


def validar_numero_nao_negativo(valor, campo, permitir_zero=True):
    """Converte um valor numerico e rejeita valores negativos ou nao finitos."""
    try:
        numero = float(valor)
    except (TypeError, ValueError, OverflowError):
        raise ValueError(f"{campo} deve ser um numero valido.") from None

    if not math.isfinite(numero) or numero < 0:
        raise ValueError(f"{campo} nao pode ser negativo ou infinito.")
    if not permitir_zero and numero == 0:
        raise ValueError(f"{campo} deve ser maior que zero.")
    return numero
