"""Entidades usadas pelo sistema, separadas por módulo."""

from .caminhao import Caminhao
from .compra import Compra
from .despesa import Despesa
from .produto import Produto
from .pulverizacao import Pulverizacao
from .venda_ceasa import VendaCeasa

__all__ = [
    "Caminhao",
    "Compra",
    "Despesa",
    "Produto",
    "Pulverizacao",
    "VendaCeasa",
]
