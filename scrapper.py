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
try:
    conexion = mysql.connector.connect(
        host='34.55.239.176',        # Ej: '34.67.xx.xx'
        user='root',
        password='Salasmartinez23',
        database='estadisticas'
    )
    cursor = conexion.cursor()
except mysql.connector.Error as err:
    print(f"Error al conectar a la base de datos: {err}")
    driver.quit()
    exit(1)

# URL de la página de clubes
url = 'https://www.basquetcatala.cat/clubs'

def esperar_elemento(selector, tipo='css'):
    if tipo == 'css':
        return WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

def guardar_estadisticas(nom, pj, min, min_p, pts, pts_p, fc_p, tl, t2, t3):
    try:
        sql = """
            INSERT INTO estadisticas_equipo (nom, pj, min, min_p, pts, pts_p, fc_p, tl, t2, t3)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (nom, pj, min, min_p, pts, pts_p, fc_p, tl, t2, t3)
        cursor.execute(sql, valores)
        conexion.commit()
        print(f"✅ Estadísticas de {nom} guardadas correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al guardar las estadísticas en la base de datos: {err}")

def obtener_clubes():
    try:
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
    except Exception as e:
        print(f"Error al obtener los clubes: {e}")
        return []

def obtener_estadisticas_club(club_url, club_name):
    try:
        driver.get(club_url)
        esperar_elemento('a[href^="/estadistiques/equip/"]')  # Espera el enlace para las estadísticas del equipo
        link_estadisticas = driver.find_element(By.CSS_SELECTOR, 'a[href^="/estadistiques/equip/"]')
        link_estadisticas.click()  # Hace clic en el enlace de las estadísticas del equipo

        # Espera hasta que cargue la página de estadísticas
        esperar_elemento('your-statistics-selector')  # Reemplaza con el selector real de las estadísticas

        stats = driver.find_elements(By.CSS_SELECTOR, 'your-statistics-selector')  # Reemplaza con el selector real

        if len(stats) >= 9:
            pj = int(stats[0].text) if stats[0].text.isdigit() else 0
            min = int(stats[1].text) if stats[1].text.isdigit() else 0
            min_p = float(stats[2].text) if stats[2].text.replace('.', '', 1).isdigit() else 0.0
            pts = int(stats[3].text) if stats[3].text.isdigit() else 0
            pts_p = float(stats[4].text) if stats[4].text.replace('.', '', 1).isdigit() else 0.0
            fc_p = float(stats[5].text) if stats[5].text.replace('.', '', 1).isdigit() else 0.0
            tl = stats[6].text if stats[6].text else '0'
            t2 = stats[7].text if stats[7].text else '0'
            t3 = stats[8].text if stats[8].text else '0'

            guardar_estadisticas(club_name, pj, min, min_p, pts, pts_p, fc_p, tl, t2, t3)
        else:
            print(f"Error: No se encontraron suficientes estadísticas para el club {club_name}")
    except Exception as e:
        print(f"Error al obtener estadísticas para el club {club_name}: {e}")

# Flujo principal
clubes_usuario_1 = obtener_clubes()
if clubes_usuario_1:
    club_url = clubes_usuario_1[0]['club_url']
    club_name = clubes_usuario_1[0]['club_name']
    obtener_estadisticas_club(club_url, club_name)
else:
    print("No se pudo obtener la lista de clubes.")

# Cierra conexiones al final
driver.quit()
cursor.close()
conexion.close()
