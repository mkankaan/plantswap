import re

registration_restrictions = { "min_username": 3, "max_username": 20, "min_password": 8, "max_password": 100 }

new_listing_restrictions = { "max_name": 30, "max_info": 500 }

listing_comment_restrictions = { "max_comment": 500 }

form_hint_text = {
    "username": f"Pituus {registration_restrictions['min_username']}-{registration_restrictions['max_username']} merkkiä",
    "password": f"Pituus {registration_restrictions['min_password']}-{registration_restrictions['max_password']} merkkiä ja vähintään yksi kirjain, numero ja erikoismerkki",
    "comment": f"Korkeintaan {listing_comment_restrictions['max_comment']} merkkiä"
}

def validate_username(username):
    min_length = registration_restrictions["min_username"]
    max_length = registration_restrictions["max_username"]

    if not min_length <= len(username) <= max_length:
        message = "Käyttäjätunnuksen on oltava vähintään " + str(min_length) + " ja korkeintaan " + str(max_length) + " merkkiä pitkä"
        return (False, message)

    if len(username) != len(username.replace(" ", "")):
        message = "Käyttäjätunnus ei saa sisältää välilyöntejä"
        return (False, message)
    
    if not re.search(r'[A-Za-z]{1,}', username):
        message = "Käyttäjätunnuksen täytyy sisältää vähintään yksi kirjain"
        return (False, message)
    
    if not (re.fullmatch(r'^[A-Za-z0-9]*$', username) or re.fullmatch(r'^[A-Za-z]*$', username)):
        message = "Käyttäjätunnuksessa saa olla vain kirjaimia ja numeroita"
        return (False, message)
    
    return (True, "")

def validate_password(password):
    min_length = registration_restrictions["min_password"]
    max_length = registration_restrictions["max_password"]

    if not min_length <= len(password) <= max_length:
        message = "Salasanan on oltava vähintään " + str(min_length) + " ja korkeintaan " + str(max_length) + " merkkiä pitkä"
        return (False, message)
    
    if not re.match(r'^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#%&=+-_?^])', password):
        message = "Salasanan täytyy sisältää vähintään yksi kirjain, yksi numero ja yksi erikoismerkki"
        return (False, message)
    
    return (True, "")
