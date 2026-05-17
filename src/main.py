import sys
import os
from dotenv import load_dotenv

# Configiração de caminhos (Ponto de partida)
caminho_atual = os.path.abspath(__file__)
pasta_src = os.path.dirname(caminho_atual)
raiz_projeto = os.path.dirname(pasta_src)

# Variaveis ambientes
caminho_env = os.path.join(raiz_projeto, '.env')
load_dotenv(caminho_env)

# Importando modulos
from dotenv import load_dotenv
from src.core.navegador import iniciar_navegador
from src.core.excel import carregamento_tratamento_dados
from src.bot.acoes import realizar_login, emitir_nf

# Caminhos globais para arquivos do projeto
caminho_planilha = os.path.join(raiz_projeto, 'data', 'NotasEmitir.xlsx')
caminho_login = os.path.join(raiz_projeto, 'web', 'login.html')
pasta_output = os.path.join(raiz_projeto, 'output')


def principal():
    # Carrega variaveis de ambiente
    login = os.getenv('LOGIN_USER')
    senha = os.getenv('LOGIN_PASS')
    
    # Execução do código pricipal
    nav = iniciar_navegador()
    dados_validos, dados_excluidos = carregamento_tratamento_dados(caminho_planilha)
    
    
    try:
        realizar_login(nav, caminho_login, login, senha)

        for cliente in dados_validos.itertuples():
            try:
                emitir_nf(nav, cliente)
                print(f'Nota de {cliente.Cliente} emitida com sucesso')
                nav.refresh()
            except Exception as e:
                print(f'Erro ao processar o cliente {cliente.Cliente}: {e}')
                realizar_login(nav, caminho_login, login, senha)
                continue
    finally:
            # O que fazer com dados excluidos
        if not dados_excluidos.empty:
            caminho_relatorio = os.path.join(pasta_output, 'clientes_erro_cadastro.xlsx')

            if not os.path.exists(pasta_output):
                os.makedirs(pasta_output)

            print('\n' + '-' * 50)
            print(f'[AVISO] {len(dados_excluidos)} linhas foram ignoradas por dados invalidos')
            dados_excluidos.to_excel(caminho_relatorio, index=False)
            print(f'A lista de clientes ignorados foi salva em: {caminho_relatorio}"')
            print('-' * 50)

        print('\nProcesso finalizado, fechando navegador')
        nav.quit()

if __name__== '__main__':
    principal()