import re

registration_restrictions = { "min_username": 3, "max_username": 20, "min_password": 8, "max_password": 100 }

new_listing_restrictions = { "max_name": 30, "max_info": 5000 }

listing_comment_restrictions = { "max_comment": 5000 }

def validate_username(username):
    if len(username) != len(username.replace(" ", "")):
        message = "Käyttäjätunnus ei saa sisältää välilyöntejä"
        return (False, message)
    
    if not re.search(r'[A-Za-z]{1,}', username):
        message = "Käyttäjätunnuksessa on oltava vähintään yksi kirjain"
        return (False, message)
    
    if not (re.fullmatch(r'^[A-Za-z0-9]*$', username) or re.fullmatch(r'^[A-Za-z]*$', username)):
        message = "Käyttäjätunnuksessa saa olla vain kirjaimia ja numeroita"
        return (False, message)
    
    return (True, "")