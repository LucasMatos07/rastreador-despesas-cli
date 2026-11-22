# 💰 Rastreador de Despesas & Fluxo de Caixa

Sistema de controle financeiro pessoal desenvolvido de forma incremental, evoluindo de uma aplicação de linha de comando (CLI) em Python para uma arquitetura Full-Stack com banco de dados relacional e interface Web.

---

## 🚀 Funcionalidades Atuais (v3.0 - Banco de Dados SQLite)

- **Persistência em Banco Relacional:** Armazenamento estruturado em **SQLite** (`financas.db`) com criação automática de tabela e restrições de integridade (`PRIMARY KEY`, `AUTOINCREMENT`, `NOT NULL` e `CHECK`).
- **Padrão Repository:** Isolamento completo das consultas SQL na camada de acesso a dados (`armazenamento.py`), desacoplando o banco das regras de negócio e da interface CLI.
- **Entradas e Saídas:** Registro de receitas e despesas com formatação automática de texto, validação de valores e carimbo automático de data (armazenada em ISO `AAAA-MM-DD` para ordenação exata e exibida em `DD/MM/AAAA`).
- **Resumo Consolidado via SQL:** Cálculo em tempo real do total de entradas, total de saídas e saldo atual utilizando funções de agregação (`SUM` e `COALESCE`).
- **Extrato Cronológico e Relatórios:** Listagem ordenada diretamente pelo banco (`ORDER BY`), relatório filtrado apenas com despesas (`WHERE`) e exclusão permanente por **ID** único.
- **Exportação para Planilha:** Geração de relatório (`extrato_financeiro.csv`) com IDs e formatação compatível com Excel.

---

## 🏗️ Arquitetura do Projeto

```text
rastreador-despesas-cli/
├── main.py             # Interface CLI, menus, validações e controle de tela
├── gerenciador.py      # Regras de negócio e conversão de datas (ISO <-> BR)
├── armazenamento.py    # Camada Repository: conexão SQLite, queries SQL e exportação CSV
├── .gitignore          # Ignora bancos locais (*.db), relatórios (*.csv) e cache do Python
└── README.md           # Documentação do projeto
```

---

## 🗺️ Roadmap de Evolução

- [x] **v1.0 (MVP):** CLI básico em Python com armazenamento em memória.
- [x] **v2.0 (Fluxo de Caixa):** Entradas e saídas, data automática (`DD/MM/AAAA`), cálculo de saldo, extrato cronológico, persistência em JSON e exportação para `.csv`.
- [x] **v3.0 (Banco de Dados SQLite):** Migração da persistência para **SQLite** (`sqlite3`) utilizando o padrão Repository.
- [ ] **v3.1 (Relatórios Avançados):** Filtros SQL por mês/ano, categoria e intervalo de datas.
- [ ] **v4.0 (Full-Stack Web & PostgreSQL):** Migração para **PostgreSQL**, API REST em **Node.js (Express)** e dashboard visual em **HTML5, CSS3 e JavaScript**.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3 (módulos nativos `sqlite3`, `csv`, `datetime` e `os`)
- **Banco de Dados & Ferramentas:** SQLite (`financas.db`) e DB Browser for SQLite
- **Arquitetura:** Modular em 3 camadas com Padrão Repository
- **Versionamento:** Git & GitHub (Git Flow com *branches* de *feature* e *tags* de lançamento)
- **Próximas etapas:** PostgreSQL, Node.js (Express), HTML5, CSS3 e JavaScript

---

## ▶️ Como Executar

```bash
git clone [https://github.com/LucasMatos07/rastreador-despesas-cli.git](https://github.com/LucasMatos07/rastreador-despesas-cli.git)
cd rastreador-despesas-cli
python main.py
```