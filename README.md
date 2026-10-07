# Sistema integrado de gestão do tomate

O projeto reúne a gestão da produção, logística e tarefas com o controle
financeiro de insumos, compras, despesas e vendas.

## Como executar

Na pasta do projeto, execute:

```powershell
python main.py
```

Também são aceitos `python cli.py`, `python sistema_gestao_tomate.py` e
`python -m gestao_tomate`. Todos abrem o mesmo menu integrado.

## Organização

- `interface/`, `itens/` e `estruturas/`: menu e recursos de produção,
  estoque, aplicações, cargas, rotas, vendas e tarefas.
- `core/`: regras de negócio e persistência do sistema de produção.
- `gestao_tomate/`: controle financeiro em SQLite e seus modelos.
- `dados_tomate.json`: dados de produção, carregados e salvos pelo sistema
  modular.
- `estoque.db`: banco SQLite criado pelo controle financeiro na primeira
  utilização da opção 20.

As duas bases de dados são mantidas separadas para preservar os registros
existentes e evitar duplicar ou misturar vendas, despesas e estoques com
estruturas diferentes. A opção 20 abre o controle financeiro e, ao sair dele,
retorna ao menu integrado.
