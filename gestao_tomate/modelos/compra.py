"""Modelo de uma entrada de produto comprada para o estoque."""

from dataclasses import dataclass


@dataclass
class Compra:
    id: int
    data: str
    produto_id: int
    quantidade: float
    preco_unitario: float
