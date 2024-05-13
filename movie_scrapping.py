from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import random
import urllib.parse

def gerar_link_pesquisa_google(query):
    base_url = "https://www.google.com/search?"
    parametros = {'q': query}
    url = base_url + urllib.parse.urlencode(parametros, quote_via=urllib.parse.quote)
    return url

async def find_movie(movie):
    link = gerar_link_pesquisa_google(movie)


    options = Options()
    options.add_argument("--headless")
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def random_sleep():
        random_time = random.uniform(0.5, 2.0)
        time.sleep(random_time)


    driver.get(link)

    random_sleep()

    try:
        # Encontrando a div com a classe 'fOYFme'
        div_element = driver.find_element(By.CSS_SELECTOR, "div.fOYFme")

        # Encontrando o elemento 'a' dentro da div
        link_element = div_element.find_element(By.TAG_NAME, "a")

        # Obtendo o valor do atributo href
        href_value = link_element.get_attribute("href")

        return f"{movie} está disponível em {href_value}"
    
    except:
        return "Peço desculpas, mas infelizmente nenhum link encontrado..."
    
    finally:
        driver.quit()

    
    