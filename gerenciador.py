"""
Módulo Gerenciador (Regra do negócio)
Responsável por registrar movimentações, calcular saldos, ordenar extratos
cronologicamente, filtrar despesas e remover lançamentos.
"""

# Importação das funções 

from datetime import datetime
from armazenamento import (
    inicializar_banco,
    inserir_movimentacoes,
    listar_todas_movimentacoes,
    listar_apenas_despesas,
    calcular_resumo_banco,
    deletar_movimentacoes_por_id
)

# Funções

def preparar_sistema():
    """
    Garante que o banco de dados e a tabela existam ao iniciar o app.
    """
    inicializar_banco()

def conversao_data(data_iso):
    """
    Converte a data ISO '2026-11-21' para '21-11-2026'
    """
    return datetime.strptime(data_iso, "%Y-%m-%d").strftime("%d/%m/%Y")

def registrar_movimentacao(tipo, descricao, categoria, valor):
    """
    Captura a data atual em formato ISO e envia para o banco de dados
    """
    data_iso = datetime.now().strftime("%Y-%m-%d")
    inserir_movimentacoes(tipo, descricao, categoria, valor, data_iso)
    return conversao_data(data_iso)

def obter_resumo():
    """
    Retorna o total de entrada, saída e saldo
    """
    return calcular_resumo_banco()

def extrato_completo():
    """
    Busca do banco de dados o extrato completo 
    """
    registro = listar_todas_movimentacoes()
    for item in registro:
        item["data_br"] = conversao_data(item["data"])
    return registro

def relatorio_despesa():
    """
    Busca apenas a despesa no banco de dados e calcula o total gasto
    """
    despesa = listar_apenas_despesas()
    total = 0.0
    for item in despesa:
        item["data_br"] = conversao_data(item["data"])
        total += item["valor"]
    return despesa, total

def remover_movimentacoes(id_registro):
    """
    Solicita a exclusão através do ID único do banco de dodos
    """
    return deletar_movimentacoes_por_id(id_registro)