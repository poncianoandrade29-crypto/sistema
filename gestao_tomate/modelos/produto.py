"""Modelo de um produto ou insumo mantido no estoque."""

from dataclasses import dataclass


@dataclass
class Produto:
    id: int
    nome: str
    categoria: str
    quantidade: float
    unidade: str
    preco_unitario: float
