# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

## [3.0.0] - 2026-11-22
### Adicionado
- Persistência em banco de dados relacional **SQLite** (`financas.db`) com criação automática da tabela `movimentacoes`.
- Aplicação do **Padrão Repository** na camada `armazenamento.py`, isolando todas as consultas SQL.
- Restrições de integridade no banco (`PRIMARY KEY`, `AUTOINCREMENT`, `NOT NULL` e `CHECK`).
- Cálculos consolidados de entradas, saídas e saldo diretamente via SQL (`SUM` e `COALESCE`).
- Exclusão permanente de lançamentos utilizando o `ID` real do banco de dados.

### Alterado
- Armazenamento de datas convertido para o padrão ISO (`AAAA-MM-DD`) no banco, mantendo a exibição em `DD/MM/AAAA` na interface.
- Exportação `.csv` atualizada para incluir a coluna `ID` dos registros.

### Removido
- Persistência em arquivo `dados.json` e cálculos/ordenação em memória no `gerenciador.py`.

---

## [2.0.0] - 2026-11-15
### Adicionado
- Suporte a fluxo de caixa completo (entradas e saídas).
- Carimbo automático da data atual no formato brasileiro (`DD/MM/AAAA`).
- Persistência local em `dados.json` e exportação para planilha (`extrato_financeiro.csv`).
- Separação arquitetural em três módulos (`main.py`, `gerenciador.py` e `armazenamento.py`).

---

## [1.0.0] - 2026-11-10
### Adicionado
- Versão inicial (MVP) da aplicação de linha de comando (CLI) em Python com armazenamento temporário em memória.