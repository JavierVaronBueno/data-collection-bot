from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from time import sleep

# Ruta de ChromeDriver (cambia esta ruta a donde guardaste el chromedriver.exe)
chrome_driver_path = "C:/chromedriver-win64/chromedriver-win64/chromedriver.exe"

# Configuración del driver
service = Service(executable_path=chrome_driver_path)
options = webdriver.ChromeOptions()

# Ocultar que el navegador está siendo controlado por un script
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")

# Crear una nueva instancia del navegador Chrome
driver = webdriver.Chrome(service=service, options=options)

# Ejecutar un script para evitar ser detectado como Selenium
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})

# Ir a la página de Google
driver.get("https://www.google.com")

# Buscar el campo de búsqueda por nombre
search_box = driver.find_element(By.NAME, "q")

# Escribir la consulta de búsqueda
search_box.send_keys("Selenium Python")

# Simular el presionar de la tecla Enter
search_box.send_keys(Keys.RETURN)

# Esperar un poco para cargar resultados
sleep(2)

# Extraer títulos de resultados
results = driver.find_elements(By.XPATH, "//h3")

# Imprimir los títulos de los primeros resultados
for i, result in enumerate(results[:5]):
    print(f"Resultado {i+1}: {result.text}")

# Cerrar el navegador
driver.quit()
