from flask import Flask
from flask import render_template, request, redirect, session, abort, make_response, flash
import db, users, config, listings, comments, images
import sqlite3, secrets
from utils import form_validation

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
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

    if request.method == "GET":
        result = db.query("SELECT username FROM users")

        print("käyttäjät tietokannassa:")
        for user in result:
            print(user["username"])
        
        return render_template("register.html", restrictions=restrictions, filled={})
    
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        city = request.form["city"]

        filled = { "username": username, "city": city }

        if password1 != password2:
            flash("Salasanat eivät täsmää")
            return render_template("register.html", restrictions=restrictions, filled=filled)

        username_valid, username_error_message = form_validation.validate_username(username)

        if not username_valid:
            flash(username_error_message)
            return render_template("register.html", restrictions=restrictions, filled=filled)
        
        password_valid, password_error_message = form_validation.validate_password(password1)

        if not password_valid:
            flash(password_error_message)
            return render_template("register.html", restrictions=restrictions, filled=filled)
        
        try:
            users.create_user(username, password1, city)
            print("käyttäjä", username, "luotu")
            flash("Tunnuksen luonti onnistui")
            return redirect("/") # redirect to next page
        except sqlite3.IntegrityError:
            filled = { "city": city }
            flash("Käyttäjätunnus varattu")
            return render_template("register.html", restrictions=restrictions, filled=filled)

# user profile page
@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)

    if not user or user["status"] == 0:
        abort(404)
    
    listings = users.get_listings(user_id)
    return render_template("user.html", user=user, listings=listings)

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
            return("ei jpg-tiedosto")

        image = file.read()
        if len(image) > 200 * 1024:
            return("tiedosto on liian suuri")

        user_id = session["user_id"]
        user = users.get_user(user_id)

        if user["has_image"]:
            images.remove_image(user["image_id"])
            print("deleted user's image")

        images.add_image(image, user_id)
        image_id = images.newest_image_from_user(user_id)
        users.update_image(user_id, image_id)
        print("updated profile pic", image_id, "for user", user_id)
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
            return("ei jpg-tiedosto")

        image = file.read()
        if len(image) > 200 * 1024:
            return("tiedosto on liian suuri")
        
        user_id = listing["user_id"]

        if listing["has_image"]:
            images.remove_image(listing["image_id"])
            print("deleted old image")

        images.add_image(image, user_id)
        print("added image")
        image_id = images.newest_image_from_user(user_id)
        print(user_id, "added image", image_id)
        listings.update_image(listing_id, image_id)
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

    restrictions = form_validation.listing_comment_restrictions

    listing_comments = comments.get_by_listing(listing_id)

    return render_template("listing.html", listing=listing, user=user, comments=listing_comments, restrictions=restrictions)

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
    if not listing:
        abort(404)
        
    if listing["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit_listing.html", listing=listing)

    if request.method == "POST":
        check_csrf()

        name = request.form["name"]
        listings.update_listing(listing["id"], name)
        print("päivitys onnistui")
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
            listings.remove_listing(listing["id"])

            if listing["has_image"]:
                images.remove_image(listing["image_id"])
                print("deleted image")

            print("ilmoitus", listing["id"], "poistettu")
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

    print("query:", query)
    print("city:", city)

    results = []

    if query and city:
        results = listings.search_query_city(query, city)
    elif query:
        results = listings.search_query(query)
    elif city:
        results = listings.search_city(city)
    else:
        results = listings.fetch_all()

    print("results:", len(results))

    return render_template("search.html", query=query, city=city, results=results)

