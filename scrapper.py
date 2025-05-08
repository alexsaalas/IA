from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configura el servicio para Selenium
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL de la página de clubes (ya la tienes, por ejemplo, 'https://www.basquetcatala.cat/clubs')
club_urls = df_clubs['club_url']  # Asumiendo que tienes las URLs de los clubes en df_clubs

# Crear un diccionario para almacenar las categorías y equipos por club
club_data = {}

for url in club_urls:
    # Cargar la página del club
    driver.get(url)
    
    # Espera un poco a que se cargue la página
    driver.implicitly_wait(10)
    
    # Scraping de las categorías y equipos (esto depende de cómo estén estructurados en HTML)
    # Aquí un ejemplo, pero necesitarás ajustar los selectores según la página del club:
    
    categories = driver.find_elements(By.CSS_SELECTOR, '.category-class')  # Ajusta el selector CSS
    teams = driver.find_elements(By.CSS_SELECTOR, '.team-class')  # Ajusta el selector CSS
    
    category_names = [category.text.strip() for category in categories]
    team_names = [team.text.strip() for team in teams]
    
    # Guardar los datos en el diccionario
    club_data[url] = {
        'categories': category_names,
        'teams': team_names
    }
    
    # Espera un poco entre páginas para no sobrecargar el servidor
    time.sleep(2)

# Ver los resultados
print(club_data)

# Cerrar el navegador
driver.quit()
