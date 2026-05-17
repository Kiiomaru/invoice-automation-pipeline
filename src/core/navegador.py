from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

def iniciar_navegador():
    '''Configura e abre o Chrome'''
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    caminho_download = os.path.join(os.getcwd(), 'downloads_nfs')
    if not os.path.exists(caminho_download):
        os.makedirs(caminho_download)

    options.add_experimental_option("prefs", {
    "download.default_directory": caminho_download,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
    })
    
    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico, options=options)
    navegador.implicitly_wait(5)
    return navegador