from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import mysql.connector
import time

# Configura el servicio para Selenium
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Configura la conexión a la base de datos MySQL
conexion = mysql.connector.connect(
    host='34.55.239.176',        # Ej: '34.67.xx.xx'
    user='root',
    password='Salasmartinez23',
    database='estadisticas'
)
cursor = conexion.cursor()

# URL de la página de clubes
url = 'https://www.basquetcatala.cat/clubs'

def esperar_elemento(selector, tipo='css'):
    if tipo == 'css':
        return WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

def guardar_estadisticas(nom, pj, min, min_p, pts, pts_p, fc_p, tl, t2, t3):
    sql = """
        INSERT INTO estadisticas_equipo (nom, pj, min, min_p, pts, pts_p, fc_p, tl, t2, t3)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = (nom, pj, min, min_p, pts, pts_p, fc_p, tl, t2, t3)
    cursor.execute(sql, valores)
    conexion.commit()
    print(f"✅ Estadísticas de {nom} guardadas correctamente.")

def obtener_clubes():
    driver.get(url)
    esperar_elemento('a[href^="/club/"]')
    clubs = []
    links = driver.find_elements(By.CSS_SELECTOR, 'a[href^="/club/"]')
    for link in links:
        club_name = link.text.strip()
        club_url = link.get_attribute('href')
        club_id = club_url.split('/')[-1]
        clubs.append({'club_name': club_name, 'club_id': club_id, 'club_url': club_url})
    return clubs

def obtener_estadisticas_club(club_url, club_name):
    driver.get(club_url)
    esperar_elemento('your-statistics-selector')
    stats = driver.find_elements(By.CSS_SELECTOR, 'your-statistics-selector')
    
    # Ejemplo de extracción → reemplaza según los selectores reales:
    pj = int(stats[0].text)
    min = int(stats[1].text)
    min_p = float(stats[2].text)
    pts = int(stats[3].text)
    pts_p = float(stats[4].text)
    fc_p = float(stats[5].text)
    tl = stats[6].text
    t2 = stats[7].text
    t3 = stats[8].text

    guardar_estadisticas(club_name, pj, min, min_p, pts, pts_p, fc_p, tl, t2, t3)

# Flujo principal
clubes_usuario_1 = obtener_clubes()
club_url = clubes_usuario_1[0]['club_url']
club_name = clubes_usuario_1[0]['club_name']
obtener_estadisticas_club(club_url, club_name)

# Cierra conexiones al final
driver.quit()
cursor.close()
conexion.close()
