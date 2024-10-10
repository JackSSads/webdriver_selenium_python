from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException

from time import sleep
from random import randint
from typing import Union, List
from os import environ, name, path

class Driver():
    """ Fonte de opções de switches
        https://chromium.googlesource.com/chromium/src/+/master/chrome/common/chrome_switches.cc
        e
        https://peter.sh/experiments/chromium-command-line-switches/
    """

    """ Manipulação da janela:
        --start-maximized                   - Inicia maximizado
        --lang=pt-BR                        - Define o idioma de inicialização, # en-US , pt-BR
        --incognito                         - Usar o modo anônimo
        --window-size=800,800               - Define a resolução da janela em largura e altura
        --headless                          - Roda em segundo plano(com a janela fechada)
        --disable-notifications             - Desabilita notificações
        --disable-gpu                       - Desabilita renderização com GPU
    """

    """ Métodos do WebDriver:
        - .get("https://...")               - Navegar até uma página
        - .maximize_windo()                 - Maximiza a janela
        - .refresh()                        - Recarrega a página atual
        - .get(driver.current)              - Recarrega a página atual
        - .back()                           - Volta à página anterior
        - .forward()                        - Navega uma página à frente
        - .title                            - Obtém o título da página
        - .current_window_handle            - Obtém a janela atual
        - .window_handle                    - Obtém todas as janelas
        - .current_url                      - Obtém a URL da página atual
        - .switch_to.window()               - Mudar para uma nova janela
        - .page_current_source              - Obtém o código fonte da página atual
        - .find_element().text              - Obtém o texto de um elemento
        - .find_element().get_attribuite()  - Obtém o dado de uma propriedade expecífica
        - .close()                          - Fecha o navegador
    """

    def __init__(self, arguments: list = ['--window-size=900,900',]) -> None:
        self.arguments: list = arguments
        self.__driver: webdriver | None = None
        self.__wait: WebDriverWait | None = None
        self.__chrome_options: Options = Options()

    def initialize_webdriver(self) -> None:
        try:
            for argument in self.arguments:
                self.__chrome_options.add_argument(argument)

            # Para sistemas Windows
            if name == 'nt':
                downloads_folder: str = path.join(environ['USERPROFILE'], 'Downloads')
            # Para sistemas Unix (Linux, macOS)
            else:
                downloads_folder: str = path.join(environ['HOME'], 'Downloads')

            """
                Lista de opções experimentais(nem todas estão documentadas)
                https://chromium.googlesource.com/chromium/src/+/master/chrome/common/pref_names.cc
                Uso de configurações experimentais
            """
            self.__chrome_options.add_experimental_option('prefs', {
                # Alterar o local padrão de download de arquivos
                'download.default_directory': downloads_folder,
                # notificar o google chrome sobre essa alteração
                'download.directory_upgrade': True,
                # Desabilitar a confirmação de download
                'download.prompt_for_download': False,
                # Desabilitar notificações
                'profile.default_content_setting_values.notifications': 2,
                # Permitir multiplos downloads
                'profile.default_content_setting_values.automatic_downloads': 1,
            })

            # inicializando o webdriver
            if self.__driver is None:
                self.__driver = webdriver.Chrome(options=self.__chrome_options)
            
            # Instanciando Wait Explícito
            self.__wait = WebDriverWait(
                    self.__driver,
                    10,                
                    poll_frequency=1,
                    ignored_exceptions=[
                        NoSuchElementException,
                        ElementNotVisibleException,
                        ElementNotSelectableException
                    ]
                )

        except Exception as e:
            print(f"Ocorreu um erro ao iniciar o WebDriver: {e}")

    def close_web_driver(self) -> None:
        try:
            self.__driver.close()
        except Exception as e:
            print(f"Erro ao tentar fechar o navegador: {e}")

    def navigate_to(self, url: str) -> None:
        try:
            self.__driver.get(url)
        except Exception as e:
            print(f"Erro ao tentar navegar para {url}: {e}")

    def get_by_id(self, id: str) -> Union[WebElement, None]:
        try:
            return self.__driver.find_element(By.ID, id)
        except Exception as e:
            print(f"Erro ao tentar achar o elemento com ID: {e}")

    def get_by_name(self, name: str) -> Union[WebElement, None]:
        try:
            return self.__driver.find_element(By.NAME, name)
        except Exception as e:
            print(f"Erro ao tentar achar o elemento com NAME: {e}")

    def get_by_class_name(self, class_name: str) -> Union[WebElement, None]:
        try:
            return self.__driver.find_element(By.CLASS_NAME, class_name)
        except Exception as e:
            print(f"Erro ao tentar achar o elemento com CLASS_NAME: {e}")

    def get_by_link_text(self, text: str) -> Union[WebElement, None]:
        try:
            return self.__driver.find_element(By.LINK_TEXT, text)
        except Exception as e:
            print(f"Erro ao tentar achar o elemento com LINK_TEXT: {e}")

    def get_by_partial_link_text(self, partial_text: str) -> Union[WebElement, None]:
        try:
            return self.__driver.find_element(By.PARTIAL_LINK_TEXT, partial_text)
        except Exception as e:
            print(f"Erro ao tentar achar o elemento com PARTIAL_LINK_TEXT: {e}")

    def get_by_tag_name(self, tag_name: str) -> Union[WebElement, None]:
        try:
            return self.__driver.find_element(By.TAG_NAME, tag_name)
        except Exception as e:
            print(f"Erro ao tentar achar o elemento com TAG_NAME: {e}")

    def get_by_xpath(self, xpath: str) -> Union[WebElement, None]:
        try:
            return self.__driver.find_element(By.XPATH, xpath)
        except Exception as e:
            print(f"Erro ao tentar achar o elemento com XPATH: {e}")
    
    def get_by_css_selector(self, css_selector: str) -> Union[WebElement, None]:
        try:
            return self.__driver.find_element(By.CSS_SELECTOR, css_selector)
        except Exception as e:
            print(f"Erro ao tentar achar o elemento com XPATH: {e}")
   
    def click_js(self, element: WebElement) -> None:
        try:
            self.__driver.execute_script('arguments[0].click()', element)
        except Exception as e:
            print(f"Erro ao tentar clicar com JS: {e}")

    def write(self, element: WebElement, text: str, randint_a: int = 1, randint_b: int = 5, range: int = 30) -> None:
        try:
            for letter in text:
                element.send_keys(letter)
                sleep(randint(randint_a, randint_b) / range)
        except Exception as e:
            print(f"Erro ao tentar escrever: {e}")

    def scroll(self, value: str, ws: str = "scrollTo") -> None:
        try:
            self.__driver.execute_script(f"window.{ws}(0, {value});")
        except Exception as e:
            print(f"Erro ao tentar rolar a tela: {e}")

    def waiting(self, search: str, ec: EC = EC.visibility_of_element_located, get_by: By = By.XPATH,) -> Union[WebElement, List[WebElement], None]:
        try:
            return self.__wait.until(
                ec((get_by, search))
            )
        except Exception as e:
            print(f"Erro ao buscar elemento: {e}")

    def print(self, filename: str) -> None:
        try:
            self.__driver.save_screenshot(filename)
        except Exception as e:
            print(f"Erro ao realizar captura da tela: {e}")

    def keys(self, element: WebElement, key: Keys) -> None:
        try:
            element.send_keys(key)
        except Exception as e:
            print(f"Erro ao tentar usar teclas: {e}")

    def upload_file(self, element: WebElement, filepath: str) -> None:
        try:
            element.send_keys(filepath)
        except Exception as e:
            print(f"Erro ao tentar enviar arquivo: {e}")

    def open_iframe(self, element: WebElement, ) -> None:
        try:
            self.__driver.switch_to.frame(element)
        except Exception as e:
            print(f"Erro ao tentar entrar no iframe: {e}")

    def alerts(self) -> None:
        try:
            self.__driver.switch_to.alert
        except Exception as e:
            print(f"Erro ao tentar capturar alerta: {e}")

    def current_page(self) -> Union[str, None]:
        try:
            return self.__driver.current_window_handle
        except Exception as e:
            print(f"Erro ao tentar buscar janela atual: {str(e)}")
        
    def window_handles(self) -> Union[str, None]:
        try:
            return self.__driver.window_handles
        except Exception as e:
            print(f"Erro ao tentar buscar janelas abertas: {str(e)}")
    
    def switch_to(self, aba: str) -> None:
        try:
            self.__driver.switch_to.window(aba)
        except Exception as e:
            print(f"Erro ao tentar buscar janelas abertas: {str(e)}")
