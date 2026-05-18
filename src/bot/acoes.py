import time
import shutil
import os
from selenium.webdriver.common.by import By
from pathlib import Path

def limpar_pastas(pastas):
    # Limpa as pastas a cada nova automação
    for pasta in pastas:
        if os.path.exists(pasta):
            for arquivo in os.listdir(pasta):
                caminho_arquivo = os.path.join(pasta, arquivo)
                try:
                    if os.path.isfile(caminho_arquivo) or os.path.islink(caminho_arquivo):
                        os.unlink(caminho_arquivo)
                    elif os.path.isdir(caminho_arquivo):
                        shutil.rmtree(caminho_arquivo)
                except Exception as e:
                    print(f'Falha ao apagar {caminho_arquivo}. Motivo: {e}')


def realizar_login(navegador, caminho_html, login, senha):
    '''Realizar login no sistema'''
    url_final = Path(caminho_html).as_uri()
    navegador.get(url_final)
    navegador.find_element(By.XPATH, '/html/body/div/form/input[1]').send_keys(login)
    navegador.find_element(By.XPATH, '/html/body/div/form/input[2]').send_keys(senha)
    navegador.find_element(By.XPATH, '/html/body/div/form/button').click()

def destacar_erro(navegador, nome_campo, mensagem_js=None):
    '''Função auxiliar para erros'''
    campo = navegador.find_element(By.NAME, nome_campo)
    navegador.execute_script("arguments[0].style.border='3px solid red'", campo)
    navegador.execute_script("arguments[0].scrollIntoView({block: 'center'});", campo)
    if mensagem_js:
        navegador.execute_script(f"arguments[0].value='{mensagem_js}'", campo)
    time.sleep(0.5)


def emitir_nf(navegador, dados_tabela):
    '''Preenche os campos em uma nota fiscal'''
    nome_limpo = str(dados_tabela.Cliente).strip()
    cnpj_formatado = str(dados_tabela.CPF_CNPJ).replace('.0', '').strip()
    # Nome:
    navegador.find_element(By.NAME, 'nome').send_keys(nome_limpo)
    # Endereço:
    navegador.find_element(By.NAME, 'endereco').send_keys(dados_tabela.Endereço)
    # Bairro:
    navegador.find_element(By.NAME, 'bairro').send_keys(dados_tabela.Bairro)
    # Municipio:
    navegador.find_element(By.NAME, 'municipio').send_keys(dados_tabela.Municipio)
    # CEP:
    navegador.find_element(By.NAME, 'cep').send_keys(dados_tabela.CEP)
    # UF:
    navegador.find_element(By.NAME, 'uf').send_keys(dados_tabela.UF)
    # CNPJ:
    navegador.find_element(By.NAME, 'cnpj').send_keys(dados_tabela.CPF_CNPJ)
    # Inscrição Estadual:
    navegador.find_element(By.NAME, 'inscricao').send_keys(dados_tabela.Inscricao_Estadual)
    # Descrição das mercadorias/serviço prestado:
    navegador.find_element(By.NAME, 'descricao').send_keys(dados_tabela.Descrição)
    # Quantidade:
    navegador.find_element(By.NAME, 'quantidade').send_keys(dados_tabela.Quantidade)
    # Valor Unitario:
    navegador.find_element(By.NAME, 'valor_unitario').send_keys(dados_tabela.Valor_Unitario)
    # Valor Total:
    navegador.find_element(By.NAME, 'total').send_keys(dados_tabela.Valor_Total)

    '''Alguns tratamentos restantes'''
    if not nome_limpo or nome_limpo.lower() == 'nan':
        destacar_erro(navegador, 'nome', '[CAMPO VAZIO NA PLANILHA]')
        raise TypeError(f'O campo cliente está vazio')
    elif any(caracter.isdigit() for caracter in nome_limpo):
        destacar_erro(navegador, 'nome')
        raise TypeError(f'Nome não pode conter números')
    
    if len(cnpj_formatado) not in [11, 14]:
        destacar_erro(navegador, 'cnpj')
        raise ValueError(f'CPF/CNPJ inválido: {cnpj_formatado}')
    
    if len(str(dados_tabela.CEP)) != 8:
        destacar_erro(navegador, 'cep')
        raise ValueError(f'Tamanho do CEP inválido')
    
    if float(dados_tabela.Valor_Total) <= 0:
        destacar_erro(navegador, 'total')
        raise ValueError(f'Valor total não pode ser menor ou igual a 0')
    
    # clicar em emitir
    navegador.find_element(By.CLASS_NAME, 'registerbtn').click()