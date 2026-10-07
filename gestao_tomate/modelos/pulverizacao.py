"""Modelo de uma aplicação de produto no cultivo."""

from dataclasses import dataclass


@dataclass
class Pulverizacao:
    id: int
    data: str
    produto_id: int
    quantidade_usada: float
    area_talhao: str | None
