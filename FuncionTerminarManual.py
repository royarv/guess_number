def terminar_juego(input_value, intentos):
    """
    Si el usuario escribe 'terminar juego', devuelve un diccionario
    indicando que el juego ha terminado. Si no, devuelve vacío.
    """
    if isinstance(input_value, str) and input_value.lower().strip() == "terminar juego":
        return {
            "terminado": True,
            "intentos": intentos
        }
    return {"terminado": False}

