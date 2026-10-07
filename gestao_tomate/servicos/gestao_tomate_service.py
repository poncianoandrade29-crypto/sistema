"""Operações de negócio para estoque, despesas, transporte e vendas."""

from datetime import date

from gestao_tomate.banco import DB_NAME, conectar
from gestao_tomate.modelos import Produto


class GestaoTomateService:
    """Executa operações do sistema e mantém os dados consistentes."""

    def __init__(self, database=DB_NAME):
        self.database = database

    @staticmethod
    def _validar_texto(valor: str, campo: str) -> str:
        texto = valor.strip()
        if not texto:
            raise ValueError(f"{campo} não pode ficar vazio.")
        return texto

    @staticmethod
    def _validar_numero(valor: float, campo: str, permitir_zero: bool = False) -> None:
        if valor < 0 or (valor == 0 and not permitir_zero):
            comparacao = "não pode ser negativo" if permitir_zero else "deve ser maior que zero"
            raise ValueError(f"{campo} {comparacao}.")

    def cadastrar_produto(
        self,
        nome: str,
        categoria: str,
        quantidade: float,
        unidade: str,
        preco_unitario: float,
        data: str | None = None,
    ) -> int:
        """Cadastra um insumo e registra sua entrada como compra."""
        nome = self._validar_texto(nome, "Nome")
        categoria = self._validar_texto(categoria, "Categoria")
        unidade = self._validar_texto(unidade, "Unidade")
        self._validar_numero(quantidade, "Quantidade")
        self._validar_numero(preco_unitario, "Preço unitário", permitir_zero=True)
        data_compra = data or date.today().isoformat()

        with conectar(self.database) as conn:
            cursor = conn.execute(
                """
                INSERT INTO produtos (nome, categoria, quantidade, unidade, preco_unitario)
                VALUES (?, ?, ?, ?, ?)
                """,
                (nome, categoria, quantidade, unidade, preco_unitario),
            )
            produto_id = cursor.lastrowid
            conn.execute(
                """
                INSERT INTO compras (data, produto_id, quantidade, preco_unitario)
                VALUES (?, ?, ?, ?)
                """,
                (data_compra, produto_id, quantidade, preco_unitario),
            )
            return produto_id

    def registrar_compra(
        self,
        produto_id: int,
        quantidade: float,
        preco_unitario: float,
        data: str | None = None,
    ) -> None:
        """Registra uma reposição, atualizando estoque e histórico de custos."""
        self._validar_numero(quantidade, "Quantidade")
        self._validar_numero(preco_unitario, "Preço unitário", permitir_zero=True)

        with conectar(self.database) as conn:
            cursor = conn.execute(
                """
                UPDATE produtos
                SET quantidade = quantidade + ?, preco_unitario = ?
                WHERE id = ?
                """,
                (quantidade, preco_unitario, produto_id),
            )
            if cursor.rowcount == 0:
                raise ValueError("Produto não encontrado.")
            conn.execute(
                """
                INSERT INTO compras (data, produto_id, quantidade, preco_unitario)
                VALUES (?, ?, ?, ?)
                """,
                (data or date.today().isoformat(), produto_id, quantidade, preco_unitario),
            )

    def listar_estoque(self) -> list[Produto]:
        """Retorna os produtos cadastrados como objetos do modelo Produto."""
        with conectar(self.database) as conn:
            linhas = conn.execute(
                "SELECT id, nome, categoria, quantidade, unidade, preco_unitario "
                "FROM produtos ORDER BY nome"
            ).fetchall()
        return [Produto(*linha) for linha in linhas]

    def registrar_pulverizacao(
        self,
        data: str,
        produto_id: int,
        quantidade_usada: float,
        area_talhao: str,
    ) -> None:
        """Registra a aplicação e baixa o estoque em uma única transação."""
        self._validar_numero(quantidade_usada, "Quantidade aplicada")
        area_talhao = self._validar_texto(area_talhao, "Área/Talhão")

        with conectar(self.database) as conn:
            cursor = conn.execute(
                """
                UPDATE produtos
                SET quantidade = quantidade - ?
                WHERE id = ? AND quantidade >= ?
                """,
                (quantidade_usada, produto_id, quantidade_usada),
            )
            if cursor.rowcount == 0:
                existe = conn.execute(
                    "SELECT 1 FROM produtos WHERE id = ?", (produto_id,)
                ).fetchone()
                if not existe:
                    raise ValueError("Produto não encontrado.")
                raise ValueError("Quantidade insuficiente em estoque.")
            conn.execute(
                """
                INSERT INTO pulverizacoes (data, produto_id, quantidade_usada, area_talhao)
                VALUES (?, ?, ?, ?)
                """,
                (data, produto_id, quantidade_usada, area_talhao),
            )

    def registrar_despesa(
        self, data: str, descricao: str, categoria: str, valor: float
    ) -> None:
        """Salva uma despesa geral, como manutenção ou serviço agronômico."""
        descricao = self._validar_texto(descricao, "Descrição")
        categoria = self._validar_texto(categoria, "Categoria")
        self._validar_numero(valor, "Valor", permitir_zero=True)
        with conectar(self.database) as conn:
            conn.execute(
                """
                INSERT INTO despesas (data, descricao, categoria, valor)
                VALUES (?, ?, ?, ?)
                """,
                (data, descricao, categoria, valor),
            )

    def cadastrar_caminhao(
        self, placa: str, motorista: str, capacidade_caixas: int
    ) -> int:
        """Cadastra um caminhão e retorna o identificador criado."""
        placa = self._validar_texto(placa, "Placa").upper()
        motorista = self._validar_texto(motorista, "Motorista")
        self._validar_numero(capacidade_caixas, "Capacidade")
        with conectar(self.database) as conn:
            cursor = conn.execute(
                """
                INSERT INTO "caminhões" (placa, motorista, capacidade_caixas)
                VALUES (?, ?, ?)
                """,
                (placa, motorista, capacidade_caixas),
            )
            return cursor.lastrowid

    def registrar_venda_ceasa(
        self,
        data: str,
        caminhao_id: int | None,
        qtd_caixas: int,
        preco_por_caixa: float,
        custo_frete: float,
    ) -> None:
        """Registra a venda líquida de frete e valida capacidade do caminhão."""
        self._validar_numero(qtd_caixas, "Quantidade de caixas")
        self._validar_numero(preco_por_caixa, "Preço por caixa", permitir_zero=True)
        self._validar_numero(custo_frete, "Custo do frete", permitir_zero=True)
        valor_total = (qtd_caixas * preco_por_caixa) - custo_frete
        if valor_total < 0:
            raise ValueError("O frete não pode ser maior que o valor bruto da venda.")

        with conectar(self.database) as conn:
            if caminhao_id is not None:
                caminhao = conn.execute(
                    'SELECT capacidade_caixas FROM "caminhões" WHERE id = ?',
                    (caminhao_id,),
                ).fetchone()
                if caminhao is None:
                    raise ValueError("Caminhão não encontrado.")
                if qtd_caixas > caminhao[0]:
                    raise ValueError("A quantidade vendida excede a capacidade do caminhão.")
            conn.execute(
                """
                INSERT INTO vendas_ceasa
                    (data, caminhao_id, qtd_caixas, preco_por_caixa, custo_frete, valor_total)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    data,
                    caminhao_id,
                    qtd_caixas,
                    preco_por_caixa,
                    custo_frete,
                    valor_total,
                ),
            )

    def relatorio_financeiro(self) -> dict[str, float]:
        """Calcula custos de compras/despesas, faturamento líquido e resultado."""
        with conectar(self.database) as conn:
            total_insumos = conn.execute(
                "SELECT COALESCE(SUM(quantidade * preco_unitario), 0) FROM compras"
            ).fetchone()[0]
            total_despesas = conn.execute(
                "SELECT COALESCE(SUM(valor), 0) FROM despesas"
            ).fetchone()[0]
            total_vendas = conn.execute(
                "SELECT COALESCE(SUM(valor_total), 0) FROM vendas_ceasa"
            ).fetchone()[0]

        custo_total = float(total_insumos) + float(total_despesas)
        faturamento = float(total_vendas)
        return {
            "custo_insumos": float(total_insumos),
            "custo_despesas_gerais": float(total_despesas),
            "custo_total": custo_total,
            "faturamento_ceasa": faturamento,
            "lucro_liquido": faturamento - custo_total,
        }
