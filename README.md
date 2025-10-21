# 🎯 Juego de Adivinar el Número (Versión Web con Flask)

Una aplicación web desarrollada en **Python** usando el framework **Flask**, donde el usuario debe adivinar un número aleatorio entre **1 y 100**.  
El juego da pistas si el número ingresado es **mayor o menor**, guarda la sesión del jugador y muestra su **puntaje final**.

---

## 🚀 Características

- Genera un número aleatorio entre 1 y 100.  
- Mantiene el progreso del jugador mediante **sesiones Flask**.  
- Permite **reiniciar o terminar** el juego manualmente.  
- Calcula un **puntaje total** según los intentos realizados.  
- Interfaz sencilla a través del navegador.  

---

## 🧠 Requisitos

- Python 3.8 o superior  
- Librerías externas: Flask  

---

## ⚙️ Instalación y Ejecución

# Clona este repositorio
git clone https://github.com/royarv/guess_number.git

# Entra al directorio del proyecto
cd guess_number

# Crea y activa un entorno virtual (opcional, pero recomendado)
python -m venv venv
source venv/bin/activate     # En Linux/Mac
# o
venv\Scripts\activate        # En Windows

# Instala las dependencias
pip install -r requirements.txt

# Si el archivo requirements.txt no existe, puedes crearlo con:
pip freeze > requirements.txt

# Ejecuta la aplicación
python app.py

# Abre tu navegador y visita
http://127.0.0.1:5000

---

🎉 ¡Listo! Ya puedes jugar y probar tus habilidades para adivinar el número secreto 🔢
