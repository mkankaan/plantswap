import re

registration_restrictions = {"min_username": 3,
                             "max_username": 20,
                             "min_password": 8,
                             "max_password": 100,
                             "max_city": 50}

listing_restrictions = {"max_name": 50,
                        "max_info": 500}

comment_restrictions = {"max_comment": 500}

form_hint_text = {
    "username": f"""Pituus {registration_restrictions['min_username']}-
                {registration_restrictions['max_username']} merkkiä""",
    "password": f"""Pituus {registration_restrictions['min_password']}-
                {registration_restrictions['max_password']} merkkiä,
                vähintään yksi kirjain ja numero""",
    "city": f"""Korkeintaan {registration_restrictions['max_city']} merkkiä""",
    "comment": f"""Korkeintaan {comment_restrictions['max_comment']} merkkiä"""
}


def validate_username(username):
    min_length = registration_restrictions["min_username"]
    max_length = registration_restrictions["max_username"]

    if not min_length <= len(username) <= max_length:
        message = f"""Käyttäjätunnuksen on oltava vähintään {str(min_length)}
                    ja korkeintaan {str(max_length)} merkkiä pitkä"""
        return (False, message)

    if len(username) != len(username.replace(" ", "")):
        message = "Käyttäjätunnus ei saa sisältää välilyöntejä"
        return (False, message)

    if not re.search(r"[A-Za-z]{1,}", username):
        message = "Käyttäjätunnuksen täytyy sisältää vähintään yksi kirjain"
        return (False, message)

    if not (re.fullmatch(r"^[A-Za-z0-9]*$", username) or re.fullmatch(r"^[A-Za-z]*$", username)):
        message = "Käyttäjätunnuksessa saa olla vain kirjaimia ja numeroita"
        return (False, message)
    return (True, "")


def validate_password(password):
    min_length = registration_restrictions["min_password"]
    max_length = registration_restrictions["max_password"]

    if not min_length <= len(password) <= max_length:
        message = f"""Salasanan on oltava vähintään {str(min_length)}
                    ja korkeintaan {str(max_length)} merkkiä pitkä"""
        return (False, message)

    if len(password) != len(password.replace(" ", "")):
        message = "Salasana ei saa sisältää välilyöntejä"
        return (False, message)

    if not (re.match(r"^(?=.*[a-zA-Z])", password) and re.match(r"^(?=.*[0-9])", password)):
        message = "Salasanan täytyy sisältää vähintään yksi kirjain ja yksi numero."
        return (False, message)
    return (True, "")


def validate_city(city):
    max_length = registration_restrictions["max_city"]
    city = city.strip()

    if not 1 <= len(city) <= max_length:
        message = f"""Kaupungin nimen on oltava vähintään 1 ja korkeintaan
                    {str(max_length)} merkkiä pitkä"""
        return (False, message)
    return (True, "")


def validate_comment(content):
    max_length = comment_restrictions["max_comment"]

    if not content or content.strip() == "":
        message = "Kommentti ei voi olla tyhjä"
        return (False, message)

    if len(content) > max_length:
        message = "Kommentin maksimipituus on " + str(max_length) + " merkkiä"
        return (False, message)
    return (True, "")
