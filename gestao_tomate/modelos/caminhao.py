2

from dataclasses import dataclass


@dataclass
class Caminhao:
    id: int
    placa: str
    motorista: str
    capacidade_caixas: int
