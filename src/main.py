import os
from dotenv import load_dotenv
import logging
import time
from selenium.webdriver.common.by import By
from datetime import datetime
import pandas as pd

# Criar pasta de logs e screenshots se não existir
for pasta in ['logs', 'screenshots']:
    if not os.path.exists(pasta):
        os.makedirs(pasta)

# Configuração do logging
file_handler = logging.FileHandler('logs/execucao.log', mode='a', encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s', datefmt='%Y-%m-%d %Hh%Mm%Ss'))

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(message)s'))

logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, console_handler]
)

logging.info ('---Iniciando nova automação---')

# Configiração de caminhos (Ponto de partida)
caminho_atual = os.path.abspath(__file__)
pasta_src = os.path.dirname(caminho_atual)
raiz_projeto = os.path.dirname(pasta_src)

# Variaveis ambientes
caminho_env = os.path.join(raiz_projeto, '.env')
load_dotenv(caminho_env)

# Importando modulos
from src.core.navegador import iniciar_navegador
from src.core.excel import carregamento_tratamento_dados
from src.bot.acoes import realizar_login, emitir_nf, limpar_pastas

# Caminhos globais para arquivos do projeto
caminho_planilha = os.path.join(raiz_projeto, 'data', 'NotasEmitir.xlsx')
caminho_login = os.path.join(raiz_projeto, 'web', 'login.html')
pasta_output = os.path.join(raiz_projeto, 'output')


def principal():
    # Apagar pastas
    limpar_pastas(['screenshots', 'output'])

    # Carrega variaveis de ambiente
    login = os.getenv('LOGIN_USER')
    senha = os.getenv('LOGIN_PASS')
    
    # Execução do código pricipal
    nav = iniciar_navegador()
    dados_validos, dados_excluidos = carregamento_tratamento_dados(caminho_planilha)
    erros_durante_execucao = []
    contador_sucesso = 0
       
    try:
        realizar_login(nav, caminho_login, login, senha)

        for cliente in dados_validos.itertuples():
            try:
                emitir_nf(nav, cliente)
                contador_sucesso += 1
                logging.info(
                    'NF emitida | cliente=%s | index=%s',
                    cliente.Cliente,
                    cliente.Index
                )
                nav.refresh()
            except Exception as e:
                horario = datetime.now().strftime('%d%m%Y_%H%M%S')
                nome_arquivo = f'erro_{cliente.Index}_{cliente.Cliente}_{horario}.png'
                caminho_print = os.path.join('screenshots', nome_arquivo)                                   
                nav.save_screenshot(caminho_print)

                client_dict = cliente._asdict()
                client_dict['Motivo_Erro'] = str(e)
                erros_durante_execucao.append(client_dict)


                logging.error('Erro ao processar na linha %s (Cliente: %s): %s' , cliente.Index, cliente.Cliente, e)
                realizar_login(nav, caminho_login, login, senha)
                continue
    finally:
        # Juntando erros
        df_erros_robo = pd.DataFrame(erros_durante_execucao)
        relatorio_final = pd.concat([dados_excluidos, df_erros_robo], ignore_index=True)

        # O que fazer com dados excluidos
        if not relatorio_final.empty:
                if not os.path.exists(pasta_output):
                    os.makedirs(pasta_output)

                caminho_relatorio = os.path.join(pasta_output, 'relatorio_final.xlsx')
                relatorio_final.to_excel(caminho_relatorio, index=False)
                logging.info('Relatório unificado de erros salvo em: %s', caminho_relatorio)         
                       
        logging.info('---Resumo da automação---')
        logging.info('Clientes validados: %s', contador_sucesso)
        logging.info('Erros de cadastro do excel: %d', len(dados_excluidos))
        logging.info('Erros de cadastro do robô: %d', len(erros_durante_execucao))
        logging.info('Total de falhas na execução: %d', len(relatorio_final))
        logging.info('Processo finalizado, fechando navegador')
        nav.quit()

if __name__== '__main__':
    principal()