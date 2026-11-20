# 💰 Rastreador de Despesas & Fluxo de Caixa

Sistema de controle financeiro pessoal desenvolvido de forma incremental, evoluindo de uma aplicação de linha de comando (CLI) em Python para uma arquitetura Full-Stack com banco de dados relacional e interface Web.

---

## 🚀 Funcionalidades Atuais (v2.0 - Fluxo de Caixa)

- **Entradas e Saídas:** Registro completo de receitas e despesas com formatação automática de texto e validação de valores.
- **Data Automática:** Carimbo automático da data no padrão brasileiro (`DD/MM/AAAA`).
- **Resumo Consolidado:** Cálculo em tempo real do total de entradas, total de saídas e saldo atual.
- **Extrato Cronológico e Relatórios:** Listagem ordenada por data, relatório filtrado apenas com despesas e exclusão de lançamentos por índice.
- **Persistência e Exportação:** Salvamento local automático em `dados.json` e exportação de planilha (`extrato_financeiro.csv`) compatível com Excel.
- **Arquitetura Modular:** Separação entre interface CLI (`main.py`), regras de negócio (`gerenciador.py`) e camada de persistência (`armazenamento.py`), com limpeza automática do terminal entre operações.

---

## 🏗️ Arquitetura do Projeto

```text
rastreador-despesas-cli/
├── main.py             # Interface CLI, menus, validações e controle de tela
├── gerenciador.py      # Regras de negócio, cálculos de saldo, filtros e ordenação
├── armazenamento.py    # Persistência em JSON e exportação para CSV
├── .gitignore          # Ignora dados locais (dados.json, .csv) e cache do Python
└── README.md           # Documentação do projeto
```

---

## 🗺️ Roadmap de Evolução

- [x] **v1.0 (MVP):** CLI básico em Python com armazenamento em memória.
- [x] **v2.0 (Fluxo de Caixa):** Entradas e saídas, data automática (`DD/MM/AAAA`), cálculo de saldo, extrato cronológico, persistência em JSON e exportação para `.csv`.
- [ ] **v3.0 (Banco de Dados SQLite):** Migração da persistência para **SQLite** (`sqlite3`) utilizando o padrão Repository.
- [ ] **v3.1 (Relatórios Avançados):** Filtros SQL por mês/ano, categoria e intervalo de datas.
- [ ] **v4.0 (Full-Stack Web & PostgreSQL):** Migração para **PostgreSQL**, API REST em **Node.js (Express)** e dashboard visual em **HTML5, CSS3 e JavaScript**.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3 (módulos nativos `json`, `csv`, `datetime` e `os`)
- **Persistência e Exportação Atual:** JSON e CSV
- **Versionamento:** Git & GitHub (Git Flow com *branches* de *feature* e *tags* de lançamento)
- **Próximas etapas:** SQLite (`sqlite3`), PostgreSQL, Node.js (Express), HTML5, CSS3 e JavaScript

---

## ▶️ Como Executar

```bash
git clone [https://github.com/LucasMatos07/rastreador-despesas-cli.git](https://github.com/LucasMatos07/rastreador-despesas-cli.git)
cd rastreador-despesas-cli
python main.py
```