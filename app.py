from flask import Flask
from flask import render_template, request, redirect, session, abort, make_response, flash
import db, users, config, listings, comments, images, cities
import sqlite3, secrets, markupsafe
from utils import form_validation, date_formatter

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/")
@app.route("/recommendations")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", filled={}, next_page=request.referrer)
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        next_page = request.form["next_page"]
        
        user_id = users.check_login(username, password)

        if user_id:
            active = users.check_status(user_id)
            print("user id:", user_id, "active:", active)

            if active:
                session["user_id"] = user_id
                session["username"] = username
                session["csrf_token"] = secrets.token_hex(16)
                return redirect(next_page)
            else:
                filled = { "username": username }
                flash("Väärä käyttäjätunnus tai salasana")
                return render_template("login.html", filled=filled, next_page=next_page)
        else:
            filled = { "username": username }
            flash("Väärä käyttäjätunnus tai salasana")
            return render_template("login.html", filled=filled, next_page=next_page)
        
@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    print("logged out")
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    restrictions = form_validation.registration_restrictions
    hint_text = form_validation.form_hint_text
    #all_cities = cities.fetch_all()
    all_cities = []

    if request.method == "GET":
        print("all cities:", all_cities)
        
        return render_template("register.html", restrictions=restrictions, cities=all_cities, hint_text=hint_text, filled={})
    
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        city = request.form["city"]

        filled = { "username": username, "city": city }

        if password1 != password2:
            flash("Salasanat eivät täsmää")
            return render_template("register.html", restrictions=restrictions, cities=all_cities, hint_text=hint_text, filled=filled)

        username_valid, username_error_message = form_validation.validate_username(username)

        if not username_valid:
            flash(username_error_message)
            return render_template("register.html", restrictions=restrictions, cities=all_cities, hint_text=hint_text, filled=filled)
        
        password_valid, password_error_message = form_validation.validate_password(password1)

        if not password_valid:
            flash(password_error_message)
            return render_template("register.html", restrictions=restrictions, cities=all_cities, hint_text=hint_text, filled=filled)
        
        try:
            users.create_user(username, password1, city)
            flash("Tunnuksen luonti onnistui. Voit nyt kirjautua sisään.")
            return redirect("/login")
        except sqlite3.IntegrityError:
            filled = { "city": city }
            flash("Käyttäjätunnus varattu")
            return render_template("register.html", restrictions=restrictions, cities=all_cities, hint_text=hint_text, filled=filled)

# user profile page
@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)

    if not user or user["status"] == 0:
        abort(404)
    
    listings = users.get_listings(user_id)

    joined_date = date_formatter.format_date(user["joined"])
    return render_template("user.html", user=user, listings=listings, joined_date=joined_date)

# edit profile
@app.route("/edit_profile/<int:user_id>", methods=["GET", "POST"])
def edit_profile(user_id):
    require_login()

    user =  users.get_user(user_id)
    if not user:
        abort(404)
        
    if user["id"] != session["user_id"]:
        abort(403)

    restrictions = form_validation.registration_restrictions
    hint_text = form_validation.form_hint_text
    all_cities = []

    if request.method == "GET":
        filled = { "username": user["username"], "city": user["city"] }

        return render_template("edit_profile.html", user=user, restrictions=restrictions, cities=all_cities, hint_text=hint_text, filled=filled)

    if request.method == "POST":
        check_csrf()

        new_username = request.form["new_username"]

        new_city = request.form["new_city"]

        filled = { "username": new_username, "city": new_city }

        username_valid, username_error_message = form_validation.validate_username(new_username)

        if not username_valid:
            flash(username_error_message)
            return render_template("edit_profile.html", user=user, restrictions=restrictions, cities=all_cities, hint_text=hint_text, filled=filled)
        
        try:
            users.update_user(user_id, new_username, new_city)
            print("käyttäjä", user_id, "päivitetty")
            flash("Muutokset tallennettu")
            session["username"] = new_username
            filled = { "username": new_username, "city": new_city }
            return render_template("edit_profile.html", user=user, restrictions=restrictions, cities=all_cities, hint_text=hint_text, filled=filled)
        except sqlite3.IntegrityError:
            flash("Käyttäjätunnus varattu")
            return render_template("edit_profile.html", user=user, restrictions=restrictions, cities=all_cities, hint_text=hint_text, filled=filled)

# change password
@app.route("/change_password/<int:user_id>", methods=["POST"])
def change_password(user_id):
    require_login()
    check_csrf()

    user =  users.get_user(user_id)

    if not user:
        abort(404)
        
    if user["id"] != session["user_id"]:
        abort(403)

    restrictions = form_validation.registration_restrictions
    hint_text = form_validation.form_hint_text
    all_cities = []

    if request.method == "POST":
        new_password1 = request.form["new_password1"]
        new_password2 = request.form["new_password2"]
        old_password = request.form["old_password"]

        filled = { "username": user["username"], "city": user["city"] }

        password_correct = users.check_login(user["username"], old_password)

        if not password_correct:
            flash("Väärä salasana")
            return render_template("edit_profile.html", user=user, restrictions=restrictions, cities=all_cities, hint_text=hint_text, filled=filled)

        if new_password1 != new_password2:
            flash("Salasanat eivät täsmää")
            return render_template("edit_profile.html", user=user, restrictions=restrictions, cities=all_cities, hint_text=hint_text, filled=filled)

        new_password_valid, new_password_error_message = form_validation.validate_password(new_password1)

        if not new_password_valid:
            flash(new_password_error_message)
            return render_template("edit_profile.html", user=user, restrictions=restrictions, cities=all_cities, hint_text=hint_text, filled=filled)
        
        if old_password == new_password1:
            flash("Uusi salasana ei voi olla sama kuin vanha salasana")
            return render_template("edit_profile.html", user=user, restrictions=restrictions, cities=all_cities, hint_text=hint_text, filled=filled)

        users.change_password(user_id, new_password1)
        print("käyttäjän", user["username"], "salasana vaihdettu")
        flash("Salasana vaihdettu")
        return render_template("edit_profile.html", user=user, restrictions=restrictions, cities=all_cities, hint_text=hint_text, filled=filled)
        


        if new_password1 != new_password2:
            flash("Salasanat eivät täsmää")
            return render_template("register.html", restrictions=restrictions, cities=all_cities, filled=filled)


        if new_password1 != new_password2:
            flash("Salasanat eivät täsmää")
            return render_template("register.html", restrictions=restrictions, cities=all_cities, filled=filled)

        username_valid, username_error_message = form_validation.validate_username(username)

        if not username_valid:
            flash(username_error_message)
            return render_template("register.html", restrictions=restrictions, cities=all_cities, filled=filled)
        
        password_valid, password_error_message = form_validation.validate_password(password1)

        if not password_valid:
            flash(password_error_message)
            return render_template("register.html", restrictions=restrictions, cities=all_cities, filled=filled)
        
        try:
            users.create_user(username, password1, city_id)
            print("käyttäjä", username, "luotu")
            flash("Tunnuksen luonti onnistui")
            return redirect("/") # redirect to next page
        except sqlite3.IntegrityError:
            filled = { "city": city_id }
            flash("Käyttäjätunnus varattu")
            return render_template("register.html", restrictions=restrictions, cities=all_cities, filled=filled)

# add profile image
@app.route("/add_profile_image", methods=["GET", "POST"])
def add_image():
    require_login()

    if request.method == "GET":
        return render_template("add_profile_image.html")

    if request.method == "POST":
        check_csrf()
        file = request.files["image"]

        if not file.filename.endswith(".jpg"):
            flash("Lähettämäsi tiedosto ei ole jpg-tiedosto")
            return redirect("/add_profile_image")

        image = file.read()

        if len(image) > 200 * 1024:
            flash("Lähettämäsi tiedosto on liian suuri")
            return redirect("/add_profile_image")

        user_id = session["user_id"]
        user = users.get_user(user_id)

        if user["has_image"]:
            images.remove_image(user["image_id"])
            print("deleted user's image")

        images.add_image(image, user_id)
        image_id = images.newest_image_from_user(user_id)
        users.update_image(user_id, image_id)
        flash("Kuvan lisääminen onnistui")
        return redirect("/user/" + str(user_id))
    
# fetch profile image
@app.route("/image/user/<int:user_id>")
def show_profile_image(user_id):
    image_id = users.get_image(user_id)
    image = images.get_image(image_id)
    
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

# remove profile image
@app.route("/remove/profile_image/<int:user_id>", methods=["GET", "POST"])
def remove_profile_image(user_id):
    require_login()

    user = users.get_user(user_id)

    if not user:
        abort(404)
        
    if user["id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_profile_image.html", user=user)

    if request.method == "POST":
        check_csrf()

        if "continue" in request.form:
            image_id = user["image_id"]
            images.remove_image(image_id)

            if user["has_image"]:
                users.remove_image(user_id)
                print("deleted image")

            print("käyttäjän", user["id"], "kuva", image_id, "poistettu")
        return redirect("/")

# add listing
@app.route("/new_listing", methods=["GET", "POST"])
def new_listing():
    require_login()

    restrictions = form_validation.new_listing_restrictions

    if request.method == "GET":
        return render_template("new_listing.html", restrictions=restrictions)
    
    if request.method == "POST":
        check_csrf()
        name = request.form["name"]
        is_cutting = request.form.getlist("cutting")
        info = request.form["info"]
        user_id = session["user_id"]

        if not name or len(name) > restrictions["max_name"]:
            print("listing name length incorrect")
            abort(403)

        if len(info) > restrictions["max_info"]:
            print("info length incorrect")
            abort(403)

        cutting = 0 if is_cutting == [] else 1

        try:
            listings.create_listing(name, user_id, cutting, info)
            listing = users.newest_listing(user_id)
            return redirect("/add_listing_image/" + str(listing))
        except:
            return "jotain meni vikaan"

# add listing image
@app.route("/add_listing_image/<int:listing_id>", methods=["GET", "POST"])
def add_listing_image(listing_id):
    require_login()

    listing = listings.get_listing(listing_id)

    if not listing:
        abort(404)
    
    if listing["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("add_listing_image.html", listing=listing)

    if request.method == "POST":
        check_csrf()
        file = request.files["image"]
        
        if not file.filename.endswith(".jpg"):
            flash("Lähettämäsi tiedosto ei ole jpg-tiedosto")
            return redirect("/add_listing_image/" + str(listing_id))

        image = file.read()

        if len(image) > 200 * 1024:
            flash("Lähettämäsi tiedosto on liian suuri")
            return redirect("/add_listing_image/" + str(listing_id))
        
        user_id = listing["user_id"]

        if listing["has_image"]:
            images.remove_image(listing["image_id"])
            print("deleted old image")

        images.add_image(image, user_id)
        print("added image")
        image_id = images.newest_image_from_user(user_id)
        print(user_id, "added image", image_id)
        listings.update_image(listing_id, image_id)
        flash("Kuvan lisääminen onnistui")
        return redirect("/listing/" + str(listing_id))
    
# listing page
@app.route("/listing/<int:listing_id>")
def show_listing(listing_id):
    listing = listings.get_listing(listing_id)

    if not listing:
        abort(404)

    listings.add_view(listing_id)
    listing = listings.get_listing(listing_id)

    user_id = listings.get_user(listing_id)
    user = users.get_user(user_id)

    date_added = date_formatter.format_date(listing["date"])
    restrictions = form_validation.listing_comment_restrictions
    hint_text = form_validation.form_hint_text["comment"]
    listing_comments = comments.get_by_listing(listing_id)

    formatted_comments = []

    for comment in listing_comments:
        formatted_comment = { 
                        "comment_id": comment["comment_id"],
                        "content": comment["content"],
                       "user_id": comment["user_id"],
                       "username": comment["username"],
                       "sent_date": date_formatter.format_date_time(comment["sent_date"]),
                       "user_status": comment["user_status"],
                       "user_has_image": comment["user_has_image"]                       }
        
        if comment["edited_date"]:
            formatted_comment["edited_date"] = date_formatter.format_date_time(comment["edited_date"])
        
        print("new comment:", formatted_comment)

        formatted_comments.append(formatted_comment)

    return render_template("listing.html", listing=listing, user=user, comments=formatted_comments, date_added=date_added, restrictions=restrictions, hint_text=hint_text)

# fetch listing image
@app.route("/image/listing/<int:listing_id>")
def show_listing_image(listing_id):
    image_id = listings.get_image_id(listing_id)
    #print("listing", listing_id, "has image", image_id)
    image = images.get_image(image_id)

    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

# edit listing
@app.route("/edit/listing/<int:listing_id>", methods=["GET", "POST"])
def edit_listing(listing_id):
    require_login()
    listing = listings.get_listing(listing_id)
    hint_text = form_validation.form_hint_text["comment"]

    if not listing:
        abort(404)
        
    if listing["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        print("cutting?", listing["cutting"])
        restrictions = form_validation.new_listing_restrictions
        return render_template("edit_listing.html", listing=listing, restrictions=restrictions, hint_text=hint_text)

    if request.method == "POST":
        check_csrf()

        name = request.form["name"]
        info = request.form["info"]
        is_cutting = 1 if request.form.getlist("cutting") else 0

        listings.update_listing(listing["id"], name, info, is_cutting)
        flash("Muokkaus onnistui")
        return redirect("/listing/" + str(listing["id"]))

# remove listing
@app.route("/remove/listing/<int:listing_id>", methods=["GET", "POST"])
def remove_listing(listing_id):
    require_login()

    listing = listings.get_listing(listing_id)

    if not listing:
        abort(404)
        
    if listing["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_listing.html", listing=listing)

    if request.method == "POST":
        check_csrf()

        if "continue" in request.form:
            comments.remove_from_listing(listing["id"])
            listings.remove_listing(listing["id"])

            if listing["has_image"]:
                images.remove_image(listing["image_id"])
                print("deleted image", listing["image_id"])

            print("ilmoitus", listing["id"], "poistettu")
        flash("Ilmoitus poistettiin")
        return redirect("/")
    
# add comment to listing
@app.route("/new_comment", methods=["POST"])
def new_comment():
    check_csrf()
    require_login()

    restrictions = form_validation.listing_comment_restrictions
    
    if request.method == "POST":
        content = request.form["content"]
        user_id = str(session["user_id"]) # ?
        listing_id = request.form["listing_id"]

        if not content or len(content) > restrictions["max_comment"]:
            print("comment length incorrect")
            abort(403)

        try:
            comments.create_comment(user_id, listing_id, content)
            print("added comment")
            return redirect("/listing/" + str(listing_id))
        except:
            return "jotain meni vikaan"
        
# edit comment
@app.route("/edit/comment/<int:comment_id>", methods=["GET", "POST"])
def edit_comment(comment_id):
    require_login()

    comment = comments.get_comment(comment_id)

    if not comment:
        abort(404)
        
    if comment["user_id"] != session["user_id"]:
        abort(403)

    restrictions = form_validation.listing_comment_restrictions

    if request.method == "GET":
        filled = { "content": comment["content"] }
        return render_template("edit_comment.html", comment=comment, restrictions=restrictions, filled=filled)

    if request.method == "POST":
        check_csrf()
        content = request.form["content"]
        comments.update_comment(comment_id, content)
        print("päivitys onnistui")
        return redirect("/listing/" + str(comment["listing_id"]))
    
# remove comment
@app.route("/remove/comment/<int:comment_id>", methods=["GET", "POST"])
def remove_comment(comment_id):
    require_login()

    comment = comments.get_comment(comment_id)

    if not comment:
        abort(404)
        
    if comment["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_comment.html", comment=comment)

    if request.method == "POST":
        check_csrf()

        if "continue" in request.form:
            comments.remove_comment(comment["id"])
            print("kommentti", comment["id"], "poistettu")
            flash("Kommentti poistettiin")
        return redirect("/")

# delete user account
@app.route("/delete_account", methods=["GET", "POST"])
def delete_account():
    require_login()

    if request.method == "GET":
        return render_template("delete_account.html")

    if request.method == "POST":
        check_csrf()
        user_id = session["user_id"]
        user = users.get_user(user_id)

        if "continue" in request.form:
            users.delete_account(user_id)
            print(user_id, "poistettu")

            if user["has_image"]:
                images.remove_image(user["image_id"])
                print("deleted user's image")

            logout()
            return redirect("/")
        return redirect("/user/" + str(user_id))
    
@app.route("/search")
def search():
    query = request.args.get("query")
    city = request.args.get("city")
    plant_type = request.args.get("type")

    if not plant_type or not (plant_type.lower() == "cutting" or plant_type.lower() == "plant"):
        plant_type = "all"
    else:
        plant_type = plant_type.lower()

    print("query:", query)
    print("city:", city)
    print("type:", plant_type)

    results = []

    if query and city:
        results = listings.search_query_city(query, city)
    elif query:
        results = listings.search_query(query)
    elif city:
        results = listings.search_city(city)
    else:
        results = listings.fetch_all()

    print()
    print("results:", len(results))

    if results:
        print("result:", results[0]["city"])

    return render_template("search.html", query=query, city=city, plant_type=plant_type, results=results)

