
"""
Módulo de Armazenamento (Persistência de Dados)
Responsável por ler e gravar as moviemntações financeiras no banco de dados SQLite
e exportar relatórios em formato CSV.
"""

# Importação das bibliotecas necessárias

import sqlite3
import csv

"""
Import sqlite3: Usado para chamar e registrar as movimentações no banco de dados
Import csv: usado para ler e escrever arquivos CSV 
"""

# Nome padrão do banco de dados onde os dados serão persistidos

NOME_BANCO = "financas.db"

# Funções

def conectar():
    """
    Abre a conexão com o arquivo do banco SQLite.
    """
    conexao = sqlite3.connect(NOME_BANCO)
    # Permite acessar colunas pelo nome (ex: linha["valor"]) além do índice 
    conexao.row_factory =   sqlite3.Row
    return conexao

def inicializar_banco(): 
    """
    Cria a tabela movimentações caso ela ainda não exista. 
    """
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movimentacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL CHECK (tipo IN ('entrada', 'saida')),
                descricao TEXT NOT NULL,
                categoria TEXT NOT NULL,
                valor REAL NOT NULL CHECK (valor > 0),
                data TEXT NOT NULL
            )
        """)
        conn.commit()

def inserir_movimentacoes(tipo, descricao, categoria, valor, data_iso):
    """
    Insere um novo lançamento no banco de dados.
    """
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO movimentacoes (tipo, descricao, categoria, valor, data)
            VALUES (?, ?, ?, ?, ?)
        """, (tipo, descricao, categoria, valor, data_iso))
        conn.commit()

    
def listar_todas_movimentacoes():
    """
    Retorna todas as movimentações ordenadas cronologicamente.
    """
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, tipo, descricao, categoria, valor, data
            FROM movimentacoes
            ORDER BY data ASC, id ASC
        """)
        return [dict(linha) for linha in cursor.fetchall()]

def listar_apenas_despesas():
    """
    Filtra diretamente no SQL apenas os registros do tipo 'saida'
    """
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, tipo, descricao, categoria, valor, data
            FROM movimentacoes
            WHERE tipo = 'saida'
            ORDER BY data ASC, id ASC
        """)
        return [dict(linha) for linha in cursor.fetchall()]

def calcular_resumo_banco():
    """
    Usa funções de agregação do SQL (SUM e COALESCE) para calcular os totais.
    """
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                COALESCE(SUM(CASE WHEN tipo = 'entrada' THEN valor ELSE 0 END), 0) AS total_entradas,
                COALESCE(SUM(CASE WHEN tipo = 'saida' THEN valor ELSE 0 END), 0) AS  total_saidas
            FROM movimentacoes 
        """)

        resultado = cursor.fetchone()
        entrada = resultado["total_entradas"]
        saidas = resultado["total_saidas"]
        saldo = entrada - saidas
        return saldo, entrada, saidas

def deletar_movimentacoes_por_id(id_registro):
    """
    Remove uma linha pelo ID único e retorna True se algum registro foi apagado.
    """
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(" DELETE FROM movimentacoes WHERE id = ?", (id_registro,))
        conn.commit()
        return cursor.rowcount > 0

def exportar_para_csv(lista_movimentacoes, nome_arquivo="extrato_financeiro.csv"):
    """
    Exporta a lista de movimentações para CSV compatível com Excel
    """
    with open(nome_arquivo, mode="w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(["ID", "Data", "Tipo", "Descricao", "Categoria", "Valor"])
        for item in lista_movimentacoes:
            escritor.writerow([
                item["id"],
                item["data_br"],
                item["tipo"],
                item["descricao"],
                item["categoria"],
                f"{item['valor']:.2f}".replace(".", ",")
            ])