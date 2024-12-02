import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from shutil import move
import pandas as pd
from datetime import datetime, timedelta


def configurar_driver(download_dir, chrome_driver_path, user_data_dir, profile_dir):
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_dir}")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    service = Service(executable_path=chrome_driver_path)
    return webdriver.Chrome(service=service, options=chrome_options)


def manejar_selector_fechas(driver, fecha_inicial, fecha_final, max_intentos=3):
    for intento in range(max_intentos):
        try:
            # Paso 1: Hacer clic en el selector de fechas
            selector_fechas = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.flex.flex-1.items-center.gap-3\\.5.rounded.border.border-solid.border-\\[\\#CFD4DA\\].bg-white.px-3\\.5.py-2.shadow-select"))
            )
            selector_fechas.click()
            time.sleep(1)

            # Paso 2: Editar las fechas
            fecha_inicio_input = driver.find_element(By.CSS_SELECTOR, "input[type='date'][max]")
            fecha_fin_input = driver.find_elements(By.CSS_SELECTOR, "input[type='date'][max]")[1]

            fecha_inicio_input.clear()
            fecha_inicio_input.send_keys(fecha_inicial)
            # fecha_fin_input.clear()
            # fecha_fin_input.send_keys(fecha_final)

            # Paso 3: Intentar hacer clic en el botón "Apply" o "Aceptar"
            botones = [
                ("Apply", "//span[text()='Apply']/ancestor::div[contains(@class, 'cursor-pointer')]"),
                ("Aceptar", "//span[text()='Aceptar']/ancestor::div[contains(@class, 'cursor-pointer')]")
            ]

            for texto_boton, xpath_boton in botones:
                try:
                    boton = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, xpath_boton))
                    )
                    boton.click()
                    print(f"Se hizo clic en el botón '{texto_boton}'")
                    break
                except TimeoutException:
                    print(f"No se encontró el botón '{texto_boton}', intentando el siguiente...")
            else:
                raise Exception("No se encontró ningún botón válido (Apply o Aceptar)")

            # Paso 4: Esperar a que se actualice la página
            time.sleep(2)

            return
        except Exception as e:
            print(f"Intento {intento + 1} fallido: {e}")
            time.sleep(2)
    raise Exception("No se pudo modificar las fechas después de varios intentos")


def cerrar_popups(driver):
    popups = [
        "//button[contains(@id, 'cookiebanner') and contains(@title, 'Accept')]",
        "//button[contains(@class, 'close') or contains(@class, 'closeBtn')]",
        "//div[contains(@class, 'popupCloseIcon')]"
    ]

    for popup in popups:
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, popup))).click()
            print(f"Cerrado popup: {popup}")
        except:
            pass


def descargar_archivo(driver, max_intentos=3):
    botones = [
        ("Descargar", "//span[text()='Descargar']"),
        ("Download", "//span[text()='Download']")
    ]

    for intento in range(max_intentos):
        for texto_boton, xpath_boton in botones:
            try:
                descargar_boton = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, xpath_boton))
                )
                driver.execute_script("arguments[0].scrollIntoView();", descargar_boton)
                time.sleep(1)
                descargar_boton.click()
                print(f"Se hizo clic en el botón '{texto_boton}'")
                return  # Si el clic fue exitoso, salimos de la función
            except ElementClickInterceptedException:
                print(f"El botón '{texto_boton}' está interceptado. Intentando hacer clic con JavaScript...")
                driver.execute_script("arguments[0].click();", descargar_boton)
                return  # Si el clic fue exitoso, salimos de la función
            except TimeoutException:
                print(f"No se encontró el botón '{texto_boton}', intentando el siguiente...")

        print(f"Intento {intento + 1} fallido. Reintentando...")
        time.sleep(2)

    raise Exception("No se pudo hacer clic en el botón de descarga después de varios intentos")


def esperar_descarga(download_dir, tiempo_espera=40):
    tiempo_inicio = time.time()
    while time.time() - tiempo_inicio < tiempo_espera:
        archivos = os.listdir(download_dir)
        if archivos and not any(f.endswith('.crdownload') for f in archivos):
            return max(archivos, key=lambda x: os.path.getctime(os.path.join(download_dir, x)))
        time.sleep(1)
    raise TimeoutException("La descarga no se completó en el tiempo esperado.")


def descargar_archivo_con_fechas_con_perfil(url, fecha_inicial, fecha_final, download_id, download_dir, chrome_driver_path, user_data_dir, profile_dir):
    driver = configurar_driver(download_dir, chrome_driver_path, user_data_dir, profile_dir)
    try:
        print(f"Intentando acceder a la URL: {url}")
        driver.get(url)
        time.sleep(7)  # Reducido el tiempo de espera para que cargue completamente
        print(f"URL actual: {driver.current_url}")

        if driver.current_url != url:
            print(f"Advertencia: no se ha cargado la URL correcta. Se ha cargado: {driver.current_url}")
        else:
            print("La URL se ha cargado correctamente.")

        cerrar_popups(driver)

        print("Manejando el selector de fechas...")
        manejar_selector_fechas(driver, fecha_inicial, fecha_final)
        print("Fechas modificadas exitosamente.")

        print("Buscando y haciendo clic en el botón de descarga...")
        descargar_archivo(driver)
        print("Esperando a que el archivo se descargue...")
        archivo_descargado = esperar_descarga(download_dir)
        nuevo_nombre = f"{download_id}.csv"  # Asumimos que el archivo descargado es un CSV
        print(f"Nuevo nombre con id: {nuevo_nombre}")
        move(os.path.join(download_dir, archivo_descargado), os.path.join(download_dir, nuevo_nombre))
        print(f"Archivo descargado y renombrado a: {nuevo_nombre}")
    except Exception as e:
        print(f"Error durante el proceso: {e}")
    finally:
        driver.quit()


def read_csv_to_dataframe(file_path):
    """
    Reads a CSV file and converts it to a pandas DataFrame.

    Args:
    file_path (str): The path to the CSV file.

    Returns:
    pandas.DataFrame: The DataFrame created from the CSV file.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        print(f"Successfully read {file_path}")
        print("\nFirst few rows of the DataFrame:")
        print(df.head())

        print("\nDataFrame Info:")
        df.info()

        return df

    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file {file_path} is empty.")
    except pd.errors.ParserError:
        print(f"Error: Unable to parse {file_path}. Please ensure it's a valid CSV file.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

    return None


def process_dataframe_and_download(df, tiempo=10):
    """
    Processes a DataFrame and calls a download function for each row,
    iterating through dates from 1800 to the current year in 10-year intervals.

    Args:
    df (pandas.DataFrame): The DataFrame to process.
    """
    current_year = datetime.now().year

    for _, row in df.iterrows():
        url = row['ENDPOINT']
        download_id = str(row['ID']).replace(':', '_')
        tipo = str(row['TIPO'])

        # Crear el directorio si no existe
        download_dir = os.path.join("C:/Users/Nabucodonosor/Downloads/", tipo)
        os.makedirs(download_dir, exist_ok=True)
        print(f"ruta: {download_dir}")

        chrome_driver_path = "C:/chromedriver-win64/chromedriver-win64/chromedriver.exe"
        user_data_dir = "C:/Users/Nabucodonosor/AppData/Local/Google/Chrome/User Data"
        profile_dir = "Profile 2"

        # Iterar desde 1800 hasta el año actual en intervalos de 10 años
        for year in range(1800, current_year + 1, tiempo):
            fecha_inicial = f"01.01.{year}"
            fecha_final = f"31.12.{min(year + 9, current_year)}"

            print(f"Descargando datos para el período: {fecha_inicial} - {fecha_final}")

            # Llamada a la función
            file_path = descargar_archivo_con_fechas_con_perfil(
                url, 
                fecha_inicial, 
                fecha_final, 
                f"{download_id}_{year}", 
                download_dir, 
                chrome_driver_path, 
                user_data_dir, 
                profile_dir
            )

            # Renombrar el archivo descargado
            if file_path and os.path.exists(file_path):
                file_extension = os.path.splitext(file_path)[1]
                new_file_name = f"{download_id}_{year}{file_extension}"
                new_file_path = os.path.join(download_dir, new_file_name)
                os.rename(file_path, new_file_path)
                print(f"Archivo renombrado y movido a: {new_file_path}")
            else:
                print(f"No se pudo renombrar el archivo para el ID: {download_id}_{year}")

            # Esperar un poco entre descargas para no sobrecargar el servidor
            time.sleep(5)


# Ejemplo de uso
if __name__ == "__main__":
    file_path = './EndPoint.csv'
    endpoints_df = read_csv_to_dataframe(file_path)

    # Asumiendo que ya tienes un DataFrame llamado 'df'
    # Si no, puedes crearlo así:
    # df = pd.read_csv('Endpoints.csv')

    process_dataframe_and_download(endpoints_df, 20)
