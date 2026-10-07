"""Modelo de uma venda de caixas de tomate no CEASA."""

from dataclasses import dataclass


@dataclass
class VendaCeasa:
    id: int
    data: str
    caminhao_id: int | None
    qtd_caixas: int
    preco_por_caixa: float
    custo_frete: float
    valor_total: float
