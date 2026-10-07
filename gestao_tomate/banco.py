"""Conexão SQLite e inicialização das tabelas do sistema."""

import sqlite3
from contextlib import contextmanager
from datetime import date
from pathlib import Path
from typing import Iterator


# Mantém o banco junto ao projeto, independentemente do diretório de execução.
DB_NAME = Path(__file__).resolve().parent.parent / "estoque.db"


@contextmanager
def conectar(database: str | Path = DB_NAME) -> Iterator[sqlite3.Connection]:
    """Abre uma conexão transacional e sempre a fecha ao sair do bloco."""
    conn = sqlite3.connect(database)
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def criar_tabelas(database: str | Path = DB_NAME) -> None:
    """Cria as tabelas usadas pelo estoque, aplicações, despesas e vendas."""
    with conectar(database) as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                quantidade REAL NOT NULL CHECK (quantidade >= 0),
                unidade TEXT NOT NULL,
                preco_unitario REAL NOT NULL CHECK (preco_unitario >= 0)
            );

            CREATE TABLE IF NOT EXISTS compras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                produto_id INTEGER NOT NULL,
                quantidade REAL NOT NULL CHECK (quantidade > 0),
                preco_unitario REAL NOT NULL CHECK (preco_unitario >= 0),
                FOREIGN KEY (produto_id) REFERENCES produtos (id)
            );

            CREATE TABLE IF NOT EXISTS pulverizacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                produto_id INTEGER NOT NULL,
                quantidade_usada REAL NOT NULL CHECK (quantidade_usada > 0),
                area_talhao TEXT,
                FOREIGN KEY (produto_id) REFERENCES produtos (id)
            );

            CREATE TABLE IF NOT EXISTS despesas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                descricao TEXT NOT NULL,
                categoria TEXT NOT NULL,
                valor REAL NOT NULL CHECK (valor >= 0)
            );

            CREATE TABLE IF NOT EXISTS "caminhões" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                placa TEXT NOT NULL UNIQUE,
                motorista TEXT NOT NULL,
                capacidade_caixas INTEGER NOT NULL CHECK (capacidade_caixas > 0)
            );

            CREATE TABLE IF NOT EXISTS vendas_ceasa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                caminhao_id INTEGER,
                qtd_caixas INTEGER NOT NULL CHECK (qtd_caixas > 0),
                preco_por_caixa REAL NOT NULL CHECK (preco_por_caixa >= 0),
                custo_frete REAL NOT NULL DEFAULT 0 CHECK (custo_frete >= 0),
                valor_total REAL NOT NULL,
                FOREIGN KEY (caminhao_id) REFERENCES "caminhões" (id)
            );
            """
        )
        # Bancos antigos não tinham histórico de compras; preserva o custo do
        # estoque existente como saldo inicial, sem repetir a migração depois.
        conn.execute(
            """
            INSERT INTO compras (data, produto_id, quantidade, preco_unitario)
            SELECT ?, p.id, p.quantidade, p.preco_unitario
            FROM produtos AS p
            WHERE p.quantidade > 0
              AND NOT EXISTS (
                  SELECT 1 FROM compras AS c WHERE c.produto_id = p.id
              )
            """,
            (date.today().isoformat(),),
        )
