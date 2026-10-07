"""Modelo de uma despesa geral do cultivo."""

from dataclasses import dataclass


@dataclass
class Despesa:
    id: int
    data: str
    descricao: str
    categoria: str
    valor: float
