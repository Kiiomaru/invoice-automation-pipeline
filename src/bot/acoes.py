from selenium.webdriver.common.by import By
from pathlib import Path

def realizar_login(navegador, caminho_html, login, senha):
    '''Realizar login no sistema'''
    url_final = Path(caminho_html).as_uri()
    navegador.get(url_final)
    navegador.find_element(By.XPATH, '/html/body/div/form/input[1]').send_keys(login)
    navegador.find_element(By.XPATH, '/html/body/div/form/input[2]').send_keys(senha)
    navegador.find_element(By.XPATH, '/html/body/div/form/button').click()


def emitir_nf(navegador, dados_tabela):
    
    '''Alguns tratamentos restantes'''
    nome_limpo = str(dados_tabela.Cliente).strip()
    if any(caracter.isdigit() for caracter in nome_limpo):
        raise TypeError(f'Nome não pode conter números')
    if len(str(dados_tabela.CEP)) != 8:
        raise ValueError(f'Tamanho do CEP inválido')
    if float(dados_tabela.Valor_Total) <= 0:
        raise ValueError(f'Valor total não pode ser menor ou igual a 0')
    tamanho_cpf = len(dados_tabela.CPF_CNPJ)
    if tamanho_cpf not in [11, 14]:
         raise ValueError(f'CPF/CNPJ incorreto')
    
    '''Preenche os campos em uma nota fiscal'''
    # Nome:
    navegador.find_element(By.NAME, 'nome').send_keys(dados_tabela.Cliente)
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
    
    # clicar em emitir
    navegador.find_element(By.CLASS_NAME, 'registerbtn').click()