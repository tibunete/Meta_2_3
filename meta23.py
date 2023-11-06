import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
#Perez Garcia Miriam Grupo: 387 Meta: Implementar proceso de Web Scraping usando Beautiful Soup
# Configuración del driver de Selenium
s = Service(ChromeDriverManager().install())
options = Options()
options.add_argument("--window-size=1020,1200")

# Inicializar el navegador
navegador = webdriver.Chrome(service=s, options=options)

# Abrir el sitio web de Amazon
navegador.get("https://www.amazon.com.mx")
time.sleep(3)

# Solicitar al usuario la palabra que desea buscar
productSearch = input("Escriba el producto a buscar: ")

# Encontrar el elemento de búsqueda en Amazon y escribir la palabra
txtSearch = navegador.find_element(By.ID, "twotabsearchtextbox")
txtSearch.send_keys(productSearch)

# Realizar la búsqueda haciendo clic en el botón de búsqueda
navegador.find_element(By.ID, "nav-search-submit-button").click()

#Funcion para que el usuario ingrese el numero de paginas que desea caputrar la informacion
def pageData():
   while True:
       try:
           number = int(input("¿Cuantas paginas quiere visitar? "))
           if number > 1:
               return number
           else:
               print("El numero debe de ser mayor a 1")
       except ValueError:
           print("ERROR: Solo ingrese numeros")

paginas = pageData()
pagina = 1

data = {"name ": [], "price ": [], "qualifi": [], "dateF ": []}
while pagina <= paginas:
    # Obtener el contenido de la página actual
    amazon = requests.get(navegador.current_url)

    # parse descompone por etiquetas
    soup = BeautifulSoup(navegador.page_source, 'html.parser')

    # Realiza la búsqueda de un elemento para extraer información
    product_list = soup.find_all('div', class_='a-section a-spacing-base')

    for product_item in product_list:
        h2 = product_item.find('span', class_='a-size-base-plus a-color-base a-text-normal')
        name = h2.text.strip() if h2 else "Sin nombre"

        span = product_item.find('span', class_='a-price-whole')
        price = span.text.strip() if span else "$0"

        span = product_item.find('span', class_='a-declarative')
        qualifi = span.text.strip() if span else "0"

        span = product_item.find('span', class_='a-color-base a-text-bold')
        dateF = span.text.strip() if span else "Sin fecha"

        data["name "].append(name)
        data["price "].append(price)
        data["qualifi"].append(qualifi)
        data["dateF "].append(dateF)

    try:
        btnNext = navegador.find_element(By.LINK_TEXT, "Siguiente")
        btnNext.click()
        time.sleep(5)  # Espera 5 segundos antes de pasar a la siguiente página
        pagina += 1
    except NoSuchElementException:
        print("No se encontró el botón 'Siguiente'. Terminando la búsqueda.")
        break

# Crear un DataFrame a partir de los datos recolectados
res_data = pd.DataFrame(data)

# Guardar los datos en un archivo CSV
res_data.to_csv("datasets/productoAmazono7.csv", index=False)

# Cerrar el navegador cuando hayas terminado
navegador.quit()
