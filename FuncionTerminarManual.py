# Si el valor de 'number' es la frase de terminación, detenemos el juego.
if isinstance(input_value, str) and input_value.lower().strip() == "terminar juego":
    GAME_ACTIVE = False
    return jsonify({
        "feedback": f"<h1>Juego terminado por el usuario. El número secreto era {SECRET_NUMBER}. ¡Gracias por jugar!</h1>",
        "game_status": "stopped",
        "guesses_made": GUESS_COUNT
    }), 200