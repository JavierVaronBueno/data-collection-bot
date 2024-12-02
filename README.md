# Proyecto de Automatización con Selenium

## 📖 Introducción
Este proyecto está diseñado para automatizar tareas web, incluyendo descargas de archivos, utilizando **Selenium**, un potente marco de automatización web. El proyecto utiliza un entorno virtual (`venv`) para gestionar dependencias, asegurando un desarrollo limpio y aislado.

---

## ✅ Requisitos previos
Antes de comenzar, asegúrate de cumplir con los siguientes requisitos:

1. **Python**: Versión 3.7 o superior.
   - [Descargar Python](https://www.python.org/downloads/)
2. **Google Chrome**: Asegúrate de tener instalada la versión más reciente de Google Chrome.
   - [Descargar Google Chrome](https://www.google.com/chrome/)
3. **ChromeDriver**: Descarga la versión de ChromeDriver compatible con tu navegador Chrome.
   - [Descargar ChromeDriver](https://chromedriver.chromium.org/downloads)
   - Nota: La versión de ChromeDriver debe coincidir con la versión instalada de Chrome.
4. **Git**: Necesario para clonar el repositorio.
   - [Instalar Git](https://git-scm.com/)

---

## 🚀 Instrucciones de Instalación

Sigue estos pasos para configurar el proyecto en tu sistema local:

### 1. Clonar el Repositorio
```bash
git clone <url_del_repositorio>
cd <nombre_del_repositorio>
```

### 2. Configurar un Entorno Virtual
Crea y activa un entorno virtual para manejar dependencias:
- En **Windows**:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
- En **macOS/Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar las Dependencias
Instala las librerías requeridas usando `pip`:
```bash
pip install selenium pandas
```

---

## ⚙️ Configuración Inicial

1. **Configurar la Ruta de ChromeDriver**:
   - Localiza el archivo `chromedriver.exe` descargado previamente.
   - Asegúrate de actualizar la ruta en el script para apuntar a la ubicación correcta de `chromedriver.exe`.

2. **Configurar el Perfil de Usuario de Chrome**:
   - Si es necesario, configura Selenium para usar tu perfil de usuario de Chrome para personalizaciones específicas.
   - Ejemplo en el script:
     ```python
     options = webdriver.ChromeOptions()
     options.add_argument("user-data-dir=C:\\Users\\TuUsuario\\AppData\\Local\\Google\\Chrome\\User Data")
     ```

3. **Ejecutar como Administrador**:
   - Para evitar problemas de permisos, ejecuta los scripts desde la terminal (CMD) con privilegios de administrador.

---

## 🖥️ Uso del Proyecto

### 1. Ejecutar el Script Principal
El script principal para la automatización es `bot.py`. Ejecútalo de la siguiente manera:
```bash
python bot.py
```

### 2. Ejecutar Pruebas
Para verificar que la configuración es correcta, ejecuta el script de pruebas:
```bash
python test_selenium.py
```

### 3. Archivo `EndPoint.csv`
- Este archivo contiene las URL o puntos de datos objetivo que el bot utiliza.
- Asegúrate de que el archivo esté correctamente formateado y ubicado en el directorio del proyecto.

---

## 🔍 Ejemplo de Ejecución

Para ejecutar el script `bot.py`, utiliza:
```bash
python bot.py
```

**Salida Esperada**:
- El bot abrirá una instancia del navegador Chrome.
- Navegará a las URL o realizará las tareas especificadas en el código.
- Las descargas o acciones configuradas se realizarán automáticamente.

---

## 📌 Notas Adicionales

1. **Compatibilidad**:
   - Verifica que la versión de ChromeDriver coincide con la versión de tu navegador Chrome para evitar errores de compatibilidad.

2. **Manejo de Errores**:
   - Soluciones a errores comunes de Selenium:
     - `SessionNotCreatedException`: Actualiza ChromeDriver a la última versión.
     - `TimeoutException`: Verifica tu conexión a internet o ajusta los tiempos de espera en el script.

3. **Consejos para Depuración**:
   - Usa declaraciones `print` o el módulo `logging` de Python para rastrear problemas durante la ejecución.
   - Consulta la [documentación oficial de Selenium](https://www.selenium.dev/documentation/) para soluciones avanzadas.

---

## 📜 Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

## 🛠️ Contribuciones
¡Contribuciones son bienvenidas! Siéntete libre de bifurcar el repositorio y enviar una solicitud de extracción.
