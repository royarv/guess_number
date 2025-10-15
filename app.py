from flask import Flask, request, render_template_string, render_template, session
from valor_random import numero_random
from FuncionTerminarManual import terminar_juego  # Función externa

app = Flask(__name__)
app.secret_key = "supersecreto123"

@app.route('/', methods=['GET', 'POST'])
def home():
    mensaje = ""

    # Inicializar variables de sesión
    if 'aciertos' not in session:
        session['aciertos'] = 0
    if 'fallos' not in session:
        session['fallos'] = 0
    if 'numero_generado' not in session:
        session['numero_generado'] = numero_random()
    if 'intentos' not in session:
        session['intentos'] = 0

    if request.method == 'POST':
        entrada = request.form.get('numero', '').strip()

        # Verificar si el usuario quiere terminar el juego
        resultado = terminar_juego(entrada, session.get('intentos', 0))
        if resultado.get("terminado"):
            # El usuario escribió "terminar juego"
            despedida_html = f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <title>Juego terminado</title>
                <style>
                    body {{ font-family: Arial; display:flex; flex-direction:column; align-items:center; justify-content:center; height:100vh; background:#f2f2f2; color:#333; }}
                    h1 {{ color:#c0392b; }}
                    p {{ font-size:18px; }}
                    a {{ margin-top:20px; padding:10px 20px; background:#4CAF50; color:white; text-decoration:none; border-radius:4px; }}
                </style>
            </head>
            <body>
                <h1>🎮 Juego terminado por el usuario</h1>
                <p>Intentos realizados: {resultado['intentos']}</p>
                <a href="/">Volver a jugar</a>
            </body>
            </html>
            """
            session.clear()
            return despedida_html

        # Si no se terminó el juego, sigue la lógica normal
        if entrada.isdigit():
            numero_ingresado = int(entrada)
            numero_generado = session['numero_generado']
            session['intentos'] += 1

            if numero_ingresado == numero_generado:
                session['aciertos'] += 1
                aciertos = session['aciertos']
                fallos = session['fallos']

                # Reiniciar todo para un nuevo juego
                session['numero_generado'] = numero_random()
                session['intentos'] = 0
                session['aciertos'] = 0
                session['fallos'] = 0

                return render_template("felicidades.html", aciertos=aciertos, fallos=fallos)
            else:
                session['fallos'] += 1
                mensaje = f"No acertaste. Tu número fue {numero_ingresado}, y el número era {numero_generado}. Intenta otra vez."
                # Generamos nuevo número para el siguiente intento
                session['numero_generado'] = numero_random()
        else:
            mensaje = "Ingresa un número válido o escribe 'terminar juego' para salir."

    # HTML del juego principal
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
            }
            button:hover { background:#45a049; }
            p { margin-top:20px; font-weight:bold; }
            .contador {
                position: absolute;
                top: 20px;
                right: 20px;
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
        <form method="POST">
            <input type="text" name="numero" placeholder="Ej: 25 o 'terminar juego'" required>
            <button type="submit">Adivinar número</button>
        </form>
        {% if mensaje %}
            <p>{{ mensaje }}</p>
        {% endif %}
        <div class="contador">
            Intentos: {{ intentos }}
        </div>
    </body>
    </html>
    """
    return render_template_string(html, mensaje=mensaje, intentos=session.get('intentos', 0))


if __name__ == '__main__':
    app.run(debug=True)