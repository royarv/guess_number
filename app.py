from flask import Flask, request, render_template_string, session
from valor_random import numero_random

app = Flask(__name__)
app.secret_key = "supersecreto123"  # necesario para usar session

@app.route('/', methods=['GET', 'POST'])
def home():
    mensaje = ""

    # Inicializar contador de intentos
    if 'intentos' not in session:
        session['intentos'] = 0

    if request.method == 'POST':
        try:
            numero_ingresado = int(request.form.get('numero'))
            numero_generado = numero_random()  # generar número nuevo en cada intento

            # Incrementar contador
            session['intentos'] += 1

            if numero_ingresado == numero_generado:
                mensaje = f"🎉 ¡Ganaste! Tu número fue {numero_ingresado} y el número generado era {numero_generado}."
            else:
                mensaje = f"❌ No acertaste. Tu número fue {numero_ingresado}, y el número generado era {numero_generado}. Intenta de nuevo."
        except ValueError:
            mensaje = "⚠️ Por favor, ingresa un número válido."

    # HTML con contador en la esquina derecha superior
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Adivina el número del 1 al 100 para ganar</title>
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
            input[type=number] { padding:10px; font-size:16px; width:80px; }
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
        <h1>Adivina el número del 1 al 100 para ganar</h1>
        <form method="POST">
            <input type="number" name="numero" min="1" max="100" required>
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
    return render_template_string(html, mensaje=mensaje, intentos=session['intentos'])


if __name__ == '__main__':
    app.run(debug=True)