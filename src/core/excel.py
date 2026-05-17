import pandas as pd

def carregamento_tratamento_dados(caminho_excel):
    '''Lê o excel e faz o tratamento de colunas numéricas'''
    tabela = pd.read_excel(caminho_excel)

    # Tratamento para dados essenciais vazios
    invalidos = tabela['Cliente'].isna() | tabela['CPF/CNPJ'].isna() | tabela['Valor Total'].isna()
    dados_excluidos = tabela[invalidos]
    tabela_valida = tabela[~invalidos].copy()

    # Renomear colunas para evitar probelmas no intertuples 
    tabela_valida = tabela_valida.rename(columns={
    'CPF/CNPJ': 'CPF_CNPJ', 
    'Inscricao Estadual': 'Inscricao_Estadual', 
    'Valor Unitario': 'Valor_Unitario', 
    'Valor Total': 'Valor_Total',
    })

    # Tratamento de números para evitar problemas
    colunas_numericas = ['CPF_CNPJ', 'CEP', 'Inscricao_Estadual', 'Quantidade', 'Valor_Unitario', 'Valor_Total']
    for coluna in colunas_numericas:
        tabela_valida[coluna] = tabela_valida[coluna].astype(str).str.replace('.0', '', regex=False)
    
    # Tratamento para NaN
    tabela_valida = tabela_valida.replace('nan', '')
    
    return tabela_valida, dados_excluidos
