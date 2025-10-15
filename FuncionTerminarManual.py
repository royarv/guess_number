# FuncionTerminarManual.py
from flask import session

def terminar_juego(input_value):
    """
    Revisa si el usuario quiere terminar el juego.
    Devuelve un diccionario con la info para mostrar y reinicia la sesión si se termina.
    """
    if isinstance(input_value, str) and input_value.lower().strip() == "terminar juego":
        numero_final = session.get('numero_objetivo', None)
        intentos = session.get('intentos', 0)
        session.clear()  # reinicia la sesión
        return {
            "terminado": True,
            "numero_final": numero_final,
            "intentos": intentos
        }
    return {"terminado": False}
