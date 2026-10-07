"""Business rules, persistence and indicators for Sistema Tomate."""

from collections import deque
import heapq
import json
import math
import os
from datetime import datetime

from comum.validacao import validar_numero_nao_negativo
from estruturas.arvore_precos import BSTPrecos
from estruturas.grafo_rotas import GrafoRotas
from estruturas.lista_encadeada import ListaEncadeada
from estruturas.min_heap import MinHeap
from estruturas.tabela_hash import TabelaHash

PASTA_SISTEMA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_DADOS = os.path.join(PASTA_SISTEMA, "dados_tomate.json")

class SistemaTomate:
    def __init__(self):
        """Cria as estruturas do sistema e carrega os dados persistidos."""
        # Array/lista de lotes e registros
        self.lotes = []
        self.vendas = []
        self.despesas = []
        self.caminhoes = []
        self.mudas = []
        self.aplicacoes = ListaEncadeada()

        # Hash: produtos/insumos
        self.produtos = TabelaHash()

        # Fila: cargas esperando expedição
        self.fila_cargas = deque()

        # Pilha: últimas atividades
        self.historico = []

        # Heap: tarefas prioritárias
        self.tarefas = MinHeap()
        self.proximo_id_carga = 1

        # Grafo: logística
        self.rotas = GrafoRotas()

        # BST: preços de venda
        self.arvore_precos = BSTPrecos()

        self.carregar()

    # ---------------- Persistência ----------------

    def _serializar(self):
        """Monta a representação JSON dos dados e estruturas do sistema."""
        return {
            "lotes": self.lotes,
            "vendas": self.vendas,
            "despesas": self.despesas,
            "caminhoes": self.caminhoes,
            "mudas": self.mudas,
            "aplicacoes": self.aplicacoes.listar(),
            "produtos": self._produtos_lista(),
            "fila_cargas": list(self.fila_cargas),
            "proximo_id_carga": self.proximo_id_carga,
            "historico": self.historico[-100:],
            "tarefas": self.tarefas.listar(),
            "rotas": self._rotas_lista(),
        }

    def salvar(self):
        """Grava o estado atual em JSON usando UTF-8."""
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
            json.dump(self._serializar(), arquivo, ensure_ascii=False, indent=2)

    def carregar(self):
        """Restaura dados existentes e reconstrói estruturas não serializadas."""
        if not os.path.exists(ARQUIVO_DADOS):
            self._dados_iniciais()
            return

        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            self.lotes = dados.get("lotes", [])
            self.vendas = dados.get("vendas", [])
            self.despesas = dados.get("despesas", [])
            self.caminhoes = dados.get("caminhoes", [])
            self.mudas = dados.get("mudas", [])

            for item in dados.get("aplicacoes", []):
                self.aplicacoes.adicionar(item)

            # A árvore é derivada das vendas, então deve ser refeita após a
            # leitura para que o menu de preços funcione também após reiniciar.
            for venda in self.vendas:
                self.arvore_precos.inserir(float(venda["preco_kg"]))

            for produto in dados.get("produtos", []):
                self.produtos.inserir(produto["codigo"], produto)

            self.fila_cargas = deque(dados.get("fila_cargas", []))
            maior_id_carga = max(
                (int(carga.get("id", 0)) for carga in self.fila_cargas),
                default=0,
            )
            self.proximo_id_carga = max(
                int(dados.get("proximo_id_carga", 1)),
                maior_id_carga + 1,
            )
            self.historico = dados.get("historico", [])

            for tarefa in dados.get("tarefas", []):
                # tarefa = [prioridade, contador, descricao]
                heapq.heappush(self.tarefas.dados, tuple(tarefa))
                self.tarefas.contador = max(
                    self.tarefas.contador, int(tarefa[1]) + 1
                )

            for rota in dados.get("rotas", []):
                self.rotas.adicionar_aresta(
                    rota["origem"], rota["destino"], rota["distancia_km"]
                )
        except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError):
            print("Aviso: arquivo de dados inválido. Iniciando dados vazios.")
            self._dados_iniciais()

    def _dados_iniciais(self):
        """Cria registros de demonstração e algumas rotas padrão."""
        self.produto_cadastrar("Fertilizante", "adubo", 20, 85.00, "kg")
        self.produto_cadastrar("Produto fitossanitário A", "defensivo", 5, 120.00, "L")
        self.produto_cadastrar("Herbicida", "controle_mato", 8, 95.00, "L")
        self.produto_cadastrar("Mangueira", "irrigacao", 100, 3.50, "m")
        self.produto_cadastrar("Cano PVC", "irrigacao", 30, 28.00, "m")
        self.produto_cadastrar("Caixa de tomate", "embalagem", 100, 8.00, "un")
        self.rotas.adicionar_aresta("Propriedade", "Galpão", 3)
        self.rotas.adicionar_aresta("Galpão", "CEASA", 18)
        self.rotas.adicionar_aresta("Propriedade", "CEASA", 20)
        self.salvar()

    # ---------------- Utilidades ----------------

    @staticmethod
    def moeda(valor):
        """Formata um número como moeda brasileira."""
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def registrar_atividade(self, texto):
        """Acrescenta uma atividade recente e mantém apenas as últimas 100."""
        self.historico.append(
            f"{datetime.now().strftime('%d/%m/%Y %H:%M')} - {texto}"
        )
        self.historico = self.historico[-100:]

    def _produtos_lista(self):
        """Achata os baldes da tabela hash em uma lista de produtos."""
        lista = []
        for balde in self.produtos.baldes:
            for _, produto in balde:
                lista.append(produto)
        return lista

    def _rotas_lista(self):
        """Serializa cada rota bidirecional apenas uma vez."""
        rotas = []
        vistos = set()
        for origem, vizinhos in self.rotas.vizinhos.items():
            for destino, distancia in vizinhos:
                chave = tuple(sorted((origem, destino)))
                if chave not in vistos:
                    vistos.add(chave)
                    rotas.append({
                        "origem": origem,
                        "destino": destino,
                        "distancia_km": distancia
                    })
        return rotas

    # ---------------- Produção / mudas ----------------

    def cadastrar_lote(self, nome, area_ha, quantidade_mudas,
                       produtividade_kg_muda):
        """Registra o lote, calcula a produção estimada e persiste os dados."""
        area_ha = validar_numero_nao_negativo(
            area_ha, "A área do lote", permitir_zero=False
        )
        total_mudas = validar_numero_nao_negativo(
            quantidade_mudas, "A quantidade de mudas", permitir_zero=False
        )
        if not total_mudas.is_integer():
            raise ValueError("A quantidade de mudas deve ser um número inteiro.")
        produtividade_kg_muda = validar_numero_nao_negativo(
            produtividade_kg_muda, "A produtividade por muda"
        )
        quantidade_mudas = int(total_mudas)
        lote = {
            "id": len(self.lotes) + 1,
            "nome": nome,
            "area_ha": area_ha,
            "quantidade_mudas": quantidade_mudas,
            "produtividade_kg_muda": produtividade_kg_muda,
            "producao_estimada_kg": quantidade_mudas * produtividade_kg_muda,
        }
        self.lotes.append(lote)
        self.mudas.append({
            "lote_id": lote["id"],
            "quantidade": quantidade_mudas,
            "data": datetime.now().strftime("%d/%m/%Y")
        })
        self.registrar_atividade(
            f"Lote {nome} cadastrado com {quantidade_mudas} mudas."
        )
        self.salvar()
        return lote

    # ---------------- Estoque ----------------

    def produto_cadastrar(self, nome, categoria, quantidade, custo_unitario, unidade):
        """Cadastra um produto e gera seu código sequencial."""
        quantidade = validar_numero_nao_negativo(
            quantidade, "A quantidade inicial"
        )
        custo_unitario = validar_numero_nao_negativo(
            custo_unitario, "O custo unitário"
        )
        codigo = f"P{len(self._produtos_lista()) + 1:03d}"
        produto = {
            "codigo": codigo,
            "nome": nome,
            "categoria": categoria,
            "quantidade": quantidade,
            "custo_unitario": custo_unitario,
            "unidade": unidade,
            "estoque_minimo": 0
        }
        self.produtos.inserir(codigo, produto)
        self.registrar_atividade(f"Produto cadastrado: {nome} ({codigo}).")
        return produto

    def movimentar_estoque(self, codigo, quantidade, tipo):
        """Registra entrada ou saída positiva sem permitir estoque negativo."""
        produto = self.produtos.buscar(codigo)
        if not produto:
            raise ValueError("Produto não encontrado.")

        quantidade = validar_numero_nao_negativo(
            quantidade, "A quantidade movimentada", permitir_zero=False
        )

        if tipo == "entrada":
            produto["quantidade"] += quantidade
        elif tipo == "saida":
            if quantidade > produto["quantidade"]:
                raise ValueError("Estoque insuficiente.")
            produto["quantidade"] -= quantidade
        else:
            raise ValueError("Tipo deve ser entrada ou saida.")

        self.registrar_atividade(
            f"Estoque: {tipo} de {quantidade} {produto['unidade']} "
            f"de {produto['nome']}."
        )
        self.salvar()

    def listar_estoque(self):
        """Lista os produtos pelo nome para facilitar a consulta."""
        return sorted(self._produtos_lista(), key=lambda p: p["nome"].lower())

    # ---------------- Pulverização ----------------

    def registrar_aplicacao(self, lote_id, produto_codigo, objetivo,
                            responsavel, observacao=""):
        """Registra uma aplicação sem recomendar doses ou receitas."""
        if not any(lote["id"] == lote_id for lote in self.lotes):
            raise ValueError("Lote não encontrado.")

        produto = self.produtos.buscar(produto_codigo)
        if not produto:
            raise ValueError("Produto não encontrado.")

        if produto["categoria"] not in (
            "defensivo", "controle_mato", "adubo", "biologico"
        ):
            raise ValueError("Produto não cadastrado como insumo agrícola.")

        registro = {
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "lote_id": lote_id,
            "produto_codigo": produto_codigo,
            "produto": produto["nome"],
            "objetivo": objetivo,
            "responsavel": responsavel,
            "observacao": observacao
        }

        self.aplicacoes.adicionar(registro)
        self.registrar_atividade(
            f"Aplicação registrada no lote {lote_id}: {produto['nome']}."
        )
        self.salvar()
        return registro

    # ---------------- Despesas ----------------

    def registrar_despesa(self, categoria, descricao, valor):
        """Registra uma despesa financeira."""
        valor = validar_numero_nao_negativo(valor, "O valor da despesa")
        despesa = {
            "data": datetime.now().strftime("%d/%m/%Y"),
            "categoria": categoria,
            "descricao": descricao,
            "valor": float(valor)
        }
        self.despesas.append(despesa)
        self.registrar_atividade(
            f"Despesa registrada: {descricao} - {self.moeda(valor)}."
        )
        self.salvar()

    # ---------------- Caminhões / logística ----------------

    def cadastrar_caminhao(self, placa, modelo, capacidade_kg,
                           custo_km, motorista):
        """Cadastra os dados de um caminhão utilizado na logística."""
        capacidade_kg = validar_numero_nao_negativo(
            capacidade_kg, "A capacidade do caminhão", permitir_zero=False
        )
        custo_km = validar_numero_nao_negativo(custo_km, "O custo por km")
        caminhao = {
            "placa": placa,
            "modelo": modelo,
            "capacidade_kg": capacidade_kg,
            "custo_km": custo_km,
            "motorista": motorista
        }
        self.caminhoes.append(caminhao)
        self.registrar_atividade(f"Caminhão {placa} cadastrado.")
        self.salvar()

    def adicionar_carga(self, destino, peso_kg, valor_frete, caminhao_placa=""):
        """Coloca uma carga no fim da fila e atribui um identificador persistente."""
        peso_kg = validar_numero_nao_negativo(
            peso_kg, "O peso da carga", permitir_zero=False
        )
        valor_frete = validar_numero_nao_negativo(valor_frete, "O valor do frete")
        carga = {
            "id": self.proximo_id_carga,
            "destino": destino,
            "peso_kg": peso_kg,
            "valor_frete": valor_frete,
            "caminhao": caminhao_placa,
            "status": "aguardando"
        }
        self.proximo_id_carga += 1
        self.fila_cargas.append(carga)
        self.registrar_atividade(
            f"Carga de {peso_kg} kg colocada na fila para {destino}."
        )
        self.salvar()

    def despachar_proxima_carga(self):
        """Remove e despacha a carga mais antiga da fila."""
        if not self.fila_cargas:
            return None
        carga = self.fila_cargas.popleft()
        carga["status"] = "despachada"
        self.registrar_atividade(
            f"Carga {carga['id']} despachada para {carga['destino']}."
        )
        self.salvar()
        return carga

    def rota(self, origem, destino):
        """Delega a busca de caminho ao grafo de rotas."""
        return self.rotas.bfs(origem, destino)

    # ---------------- Vendas CEASA ----------------

    def registrar_venda(self, comprador, destino, quantidade_kg,
                        preco_kg, frete=0):
        """Registra venda, atualiza a árvore de preços e salva os dados."""
        quantidade_kg = validar_numero_nao_negativo(
            quantidade_kg, "A quantidade vendida", permitir_zero=False
        )
        preco_kg = validar_numero_nao_negativo(preco_kg, "O preço por kg")
        frete = validar_numero_nao_negativo(frete, "O frete")
        venda = {
            "data": datetime.now().strftime("%d/%m/%Y"),
            "comprador": comprador,
            "destino": destino,
            "quantidade_kg": quantidade_kg,
            "preco_kg": preco_kg,
            "receita": quantidade_kg * preco_kg,
            "frete": frete
        }
        self.vendas.append(venda)
        self.arvore_precos.inserir(float(preco_kg))
        self.registrar_atividade(
            f"Venda para {comprador}: {quantidade_kg} kg."
        )
        self.salvar()
        return venda

    # ---------------- Indicadores ----------------

    def custo_total(self):
        """Soma despesas registradas e fretes das vendas."""
        # O estoque atual não é necessariamente despesa já realizada; por isso
        # o indicador usa somente despesas registradas + fretes de vendas.
        despesas = sum(d["valor"] for d in self.despesas)
        fretes = sum(v["frete"] for v in self.vendas)
        return despesas + fretes

    def receita_total(self):
        """Soma a receita bruta de todas as vendas registradas."""
        return sum(v["receita"] for v in self.vendas)

    def lucro_estimado(self):
        """Calcula receita menos despesas registradas e fretes."""
        return self.receita_total() - self.custo_total()

    def roi(self):
        """Calcula o retorno percentual; sem custos, retorna zero."""
        custo = self.custo_total()
        if custo <= 0:
            return 0
        return (self.lucro_estimado() / custo) * 100

    def producao_estimada_total(self):
        """Soma a produção prevista para todos os lotes."""
        return sum(l["producao_estimada_kg"] for l in self.lotes)

    def relatorio(self):
        """Exibe um resumo de produção, vendas, custos e estoque."""
        producao = self.producao_estimada_total()
        receita = self.receita_total()
        custo = self.custo_total()
        lucro = receita - custo

        print("\n" + "=" * 65)
        print("RELATÓRIO DA PRODUÇÃO DE TOMATE")
        print("=" * 65)
        print(f"Lotes cadastrados:          {len(self.lotes)}")
        print(f"Mudas cadastradas:          {sum(m['quantidade'] for m in self.mudas):,.0f}")
        print(f"Produção estimada:          {producao:,.2f} kg")
        print(f"Vendas realizadas:          {len(self.vendas)}")
        print(f"Receita total:              {self.moeda(receita)}")
        print(f"Custos/despesas registrados:{self.moeda(custo)}")
        print(f"Lucro estimado:             {self.moeda(lucro)}")
        print(f"ROI:                        {self.roi():,.2f}%")
        print(f"Cargas aguardando:          {len(self.fila_cargas)}")
        print(f"Produtos no estoque:        {len(self._produtos_lista())}")
        print("=" * 65)

    # ---------------- Tarefas ----------------

    def adicionar_tarefa(self, prioridade, descricao):
        """Registra uma tarefa de acordo com sua prioridade numérica."""
        try:
            prioridade_inteira = int(prioridade)
        except (TypeError, ValueError, OverflowError):
            raise ValueError("A prioridade deve ser um número inteiro de 1 a 5.") from None
        if prioridade_inteira != prioridade or not 1 <= prioridade_inteira <= 5:
            raise ValueError("A prioridade deve estar entre 1 (urgente) e 5 (baixa).")
        self.tarefas.inserir(prioridade_inteira, descricao)
        self.salvar()

    def proxima_tarefa(self):
        """Retira a tarefa mais urgente da heap e persiste a fila atualizada."""
        tarefa = self.tarefas.extrair_min()
        if tarefa:
            self.salvar()
        return tarefa
