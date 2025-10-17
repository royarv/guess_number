from flask import Flask, request, render_template_string, session, redirect, url_for
from valor_random import numero_random
from FuncionTerminarManual import terminar_juego  # función externa para terminar juego
from FuncionPuntaje import puntaje_total  # nueva función para el puntaje
from FuncionTerminarManual import terminar_juego  # importamos la función

app = Flask(__name__)
app.secret_key = "supersecreto123"


@app.route('/', methods=['GET', 'POST'])
def home():
    mensaje = ""

    # Inicializar contador de intentos y puntaje
    if 'intentos' not in session:
        session['intentos'] = 0
    if 'puntaje' not in session:
        session['puntaje'] = 0
    # Inicializar contador de intentos
    if 'intentos' not in session:
        session['intentos'] = 0

    if request.method == 'POST':
        input_value = request.form.get('numero', '').strip()

        # Llamar a la función externa para terminar el juego
        resultado = terminar_juego(input_value, session.get('intentos', 0))
        if resultado.get("terminado"):
            despedida_html = f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <title>Juego terminado</title>
                <style>
                    body {{
                        font-family: Arial;
                        display:flex;
                        flex-direction:column;
                        align-items:center;
                        justify-content:center;
                        height:100vh;
                        background:#f2f2f2;
                        color:#333;
                    }}
                    h1 {{ color:#c0392b; }}
                    p {{ font-size:18px; }}
                    a {{
                        margin-top:20px;
                        padding:10px 20px;
                        background:#4CAF50;
                        color:white;
                        text-decoration:none;
                        border-radius:4px;
                    }}
                </style>
            </head>
            <body>
                <h1>🎮 Juego terminado por el usuario</h1>
                <p>Intentos realizados: {resultado['intentos']}</p>
                <a href="/">Volver a jugar</a>
            </body>
            </html>
            """
            return despedida_html

        # Si no termina, seguimos con la lógica normal
        try:
            numero_ingresado = int(input_value)
            numero_generado = numero_random()
            session['intentos'] += 1

            # --- LÓGICA DE GANAR / PERDER + DISTANCIAS ---
            if numero_ingresado == numero_generado:
                # Calcular nuevo puntaje
                session['puntaje'] = puntaje_total(session.get('puntaje', 0), numero_ingresado, numero_generado)

                session['mensaje_final'] = (
                    f"🎉 ¡Ganaste! Adivinaste el número {numero_generado} en "
                    f"{session['intentos']} intentos. Puntaje total: {session['puntaje']} puntos."
                )
                session['mensaje_final'] = f"🎉 ¡Ganaste! Adivinaste el número {numero_generado} en {session['intentos']} intentos."
                session['resultado'] = "ganado"
                #hecho por Solano Bravo Basilio Uriel
            else:
                diferencia = abs(numero_ingresado - numero_generado)
                if 1 <= diferencia <= 9:
                    proximidad = "¡Muy cerca!"
                elif 10 <= diferencia <= 19:
                    proximidad = "¡Cerca!"
                elif 20 <= diferencia <= 31:
                    proximidad = "¡Lejos!"
                elif diferencia >= 32:
                    proximidad = "¡Muy lejos!"
                else:
                    proximidad = ""

                # Mensaje final de pérdida
                session['mensaje_final'] = (
                    f"No acertaste. El número correcto era {numero_generado}. {proximidad} "
                    f"Puntaje total: {session['puntaje']} puntos."
                )
                session['mensaje_final'] = f"No acertaste. El número correcto era {numero_generado}. {proximidad}"
                session['resultado'] = "perdido"

            # Redirigir a la página de resultado
            return redirect(url_for("resultado"))

        except ValueError:
            mensaje = "Por favor, ingresa un número valido o escribe 'terminar juego' para salir."

    # HTML principal
    # HTML con contador
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Adivina el número del 1 al 100</title>
        <style>
            body { 
                font-family: Arial; 
                display:flex; 
                flex-direction:column; 
                align-items:center; 
                justify-content:center; 
                height:100vh; 
                background:#f2f2f2; 
                position: relative;
            }
            h1 { color:#333; }
            form { margin-top:20px; }
            input[type=text] { padding:10px; font-size:16px; width:200px; border-radius:5px; border:1px solid #ccc; }
            input[type=text] { padding:10px; font-size:16px; width:160px; }
            button { 
                padding:10px 15px; 
                font-size:16px; 
                margin-left:10px; 
                cursor:pointer; 
                background:#4CAF50; 
                color:white; 
                border:none; 
                border-radius:4px; 
                transition: 0.2s;
            }
            button:hover { background:#45a049; transform: scale(1.05); }
            }
            button:hover { background:#45a049; }
            p { margin-top:20px; font-weight:bold; }
            .contador {
                position: absolute;
                top: 20px;
                right: 20px;
                background: linear-gradient(135deg, #333, #555);
                color: white;
                padding: 10px 15px;
                border-radius: 10px;
                font-weight: bold;
                box-shadow: 0 2px 6px rgba(0,0,0,0.3);
                text-align: right;
                background: #333;
                color: white;
                padding: 8px 12px;
                border-radius: 5px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <h1>Adivina el número del 1 al 100</h1>
        <form method="POST" target="_blank">
            <input type="text" name="numero" placeholder="Ej: 25 o 'terminar juego'" required>
            <button type="submit">Adivinar número</button>
        </form>
        {% if mensaje %}
            <p>{{ mensaje }}</p>
        {% endif %}
        <div class="contador">
            <div>Intentos: {{ intentos }}</div>
            <div style="margin-top:5px;">Puntaje: {{ puntaje }}</div>
                
        </div>
    </body>
    </html>
    """
    return render_template_string(html, mensaje=mensaje, intentos=session.get('intentos', 0), puntaje=session.get('puntaje', 0))
    return render_template_string(html, mensaje=mensaje, intentos=session.get('intentos', 0))


@app.route('/resultado')
def resultado():
    mensaje = session.get('mensaje_final', "Sin mensaje.")
    estado = session.get('resultado', "neutro")

    # Cambia color del fondo según resultado
    if estado == "ganado":
        fondo = "#b6f5c9"  # verde claro
        titulo = "¡Victoria!"
    elif estado == "perdido":
        fondo = "#f8b6b6"  # rojo claro
        titulo = "Intento fallido"
    else:
        fondo = "#eef2f3"
        titulo = "Resultado del juego"

    html_resultado = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>{titulo}</title>
        <style>
            body {{
                font-family: Arial;
                text-align: center;
                background: {fondo};
                height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }}
            h1 {{ color: #2c3e50; }}
            p {{ font-size: 18px; color: #333; }}
            a {{
                margin-top: 20px;
                padding: 10px 20px;
                background: #4CAF50;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }}
            a:hover {{ background: #388e3c; }}
        </style>
    </head>
    <body>
        <h1>{titulo}</h1>
        <p>{mensaje}</p>
        <a href="/">Volver al inicio</a>
    </body>
    </html>
    """
    return html_resultado


if __name__ == '__main__':
    app.run(debug=True)
    app.run(debug=True)

