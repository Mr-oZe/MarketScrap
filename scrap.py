import requests
from bs4 import BeautifulSoup
from time import sleep

class WebScraper:
    def __init__(self, file_path, timeout=10, retries=3):
        self.file_path = file_path
        self.urls = self.load_urls()
        self.timeout = timeout  # Tiempo de espera para las solicitudes
        self.retries = retries  # Número de reintentos
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0'
        }  # User-Agent de Firefox

    def load_urls(self):
        """Carga las URLs desde un archivo de texto."""
        try:
            with open(self.file_path, 'r') as file:
                urls = [url.strip() for url in file.readlines()]
                print("URLs cargadas:", urls)  # Verifica las URLs cargadas
                return urls
        except FileNotFoundError:
            print(f"El archivo {self.file_path} no fue encontrado.")
            return []

    def scrape_page(self, url):
        """Realiza el scraping de una página específica."""
        for attempt in range(self.retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=self.timeout)
                if response.status_code == 200:
                    print(f"URL: {url} - Código de respuesta 200 - éxito.")
                    # self.parse_content(response.text)
                    return  # Salir si la solicitud fue exitosa
                else:
                    print(f"URL: {url} - Código de respuesta {response.status_code}. No se puede realizar el scraping.")
                    return
            except requests.exceptions.Timeout:
                print(f"Tiempo de espera excedido para la URL: {url}. Intento {attempt + 1} de {self.retries}.")
            except requests.RequestException as e:
                print(f"Error al realizar la solicitud a {url}: {e}")

            sleep(2)  # Espera antes del siguiente intento

    def parse_content(self, html):
        """Analiza el contenido HTML y extrae información deseada."""
        soup = BeautifulSoup(html, 'html.parser')
        
        print(f"Title : {soup.title}")
        print(f"Title Name: {soup.title.name}")
        print(f"Title String: {soup.title.string}")

        # Aquí puedes agregar el código para extraer la información deseada
        #for title in soup.find_all('h2'):  # Cambia 'h2' por el selector que necesites
        #    print(title.get_text())
        # Aquí probamos en recolectar los href que se encuentran en la página
        for link in soup.find_all('a'):  # Cambia 'h2' por el selector que necesites
            print(link.get('href'))

    def run(self, product):
        """Ejecuta el scraping para todas las URLs cargadas con el producto especificado."""
        for url in self.urls:
            if url:  # Verifica que la URL no esté vacía
                # modified_url = url.format(product=product)  # Reemplaza {producto} con el producto ingresado
                # self.scrape_page(modified_url)
                modified_url = f"{url.replace('{producto}', product)}"  # Reemplaza {producto} con el producto ingresado
                self.scrape_page(modified_url)

# Uso de la clase WebScraper
if __name__ == "__main__":
    product = input("Por favor, ingresa el nombre del producto que deseas buscar: ")
    scraper = WebScraper('urls.txt', timeout=10, retries=3)
    scraper.run(product)
