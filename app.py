from flask import Flask
from flask import render_template, request, redirect, session, abort, make_response
import db, users, config, listings, comments
import sqlite3

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user_id = users.check_login(username, password)

        if user_id:
            active = users.check_status(user_id)
            print("user id:", user_id, "active:", active)

            if active:
                session["user_id"] = user_id
                session["username"] = username
                print("logged in as", username)
                return redirect("/")
            else:
                return "väärä tunnus tai salasana"
        else:
            return "väärä tunnus tai salasana"
        
@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    print("logged out")
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    restrictions = { "min_username": 3, "max_username": 20, "min_password": 8, "max_password": 100 }

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

        if password1 != password2:
            filled = { "username": username, "city": city }
            return render_template("register.html", restrictions=restrictions, filled=filled)
        
        if not restrictions["min_password"] <= len(password1) <= restrictions["max_password"]:
            print("password length incorrect")
            abort(403)
        
        if not restrictions["min_username"] <= len(username) <= restrictions["max_username"]:
            print("username length incorrect")
            abort(403)

        try:
            users.create_user(username, password1, city)
            print("käyttäjä", username, "luotu")
            return redirect("/")
        except sqlite3.IntegrityError:
            return "käyttäjätunnus varattu"

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
        file = request.files["image"]
        if not file.filename.endswith(".jpg"):
            return("ei jpg-tiedosto")

        image = file.read()
        if len(image) > 100 * 1024:
            return("tiedosto on liian suuri")

        user_id = session["user_id"]
        users.update_image(user_id, image)
        return redirect("/user/" + str(user_id))
    
# fetch profile image
@app.route("/image/user/<int:user_id>")
def show_profile_image(user_id):
    image = users.get_image(user_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

# add listing
@app.route("/new_listing", methods=["GET", "POST"])
def new_listing():
    require_login()

    restrictions = { "max_name": 30, "max_info": 5000 }

    if request.method == "GET":
        return render_template("new_listing.html", restrictions=restrictions)
    
    if request.method == "POST":
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
        file = request.files["image"]
        if not file.filename.endswith(".jpg"):
            return("ei jpg-tiedosto")

        image = file.read()
        if len(image) > 200 * 1024:
            return("tiedosto on liian suuri")

        listings.update_image(listing_id, image)
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

    restrictions = { "max_comment": 5000 }

    listing_comments = comments.get_by_listing(listing_id)

    return render_template("listing.html", listing=listing, user=user, comments=listing_comments, restrictions=restrictions)

# fetch listing image
@app.route("/image/listing/<int:listing_id>")
def show_listing_image(listing_id):
    image = listings.get_image(listing_id)
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
        if "continue" in request.form:
            listings.remove_listing(listing["id"])
            print("ilmoitus", listing["id"], "poistettu")
        return redirect("/")
    
# add comment to listing
@app.route("/new_comment", methods=["POST"])
def new_comment():
    require_login()

    restrictions = { "max_content": 5000 } # siirrä
    
    if request.method == "POST":
        content = request.form["content"]
        user_id = str(session["user_id"]) # ?
        listing_id = request.form["listing_id"]

        if not content or len(content) > restrictions["max_content"]:
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

    restrictions = { "max_content": 5000 } # siirrä

    if request.method == "GET":
        filled = { "content": comment["content"] }
        return render_template("edit_comment.html", comment=comment, restrictions=restrictions, filled=filled)

    if request.method == "POST":
        content = request.form["content"]
        comments.update_comment(comment_id, content)
        print("päivitys onnistui")
        return redirect("/listing/" + str(comment["listing_id"]))

# delete user account
@app.route("/delete_account", methods=["GET", "POST"])
def delete_account():
    require_login()

    if request.method == "GET":
        return render_template("delete_account.html")

    if request.method == "POST":
        user_id = session["user_id"]

        if "continue" in request.form:
            users.delete_account(user_id)
            print(user_id, "poistettu")
            logout()
            return redirect("/")
        return redirect("/user/" + str(user_id))
    
@app.route("/search")
def search():
    query = request.args.get("query")
    city = request.args.get("city")
    type_selection = request.args.get("type")

    print("query:", query)
    print("city:", city)

    type_cutting = 1 if type_selection == "cutting" else None
    type_full = 1 if type_selection == "full" else None

    if type_cutting is None and type_full is None:
        type_all = 1

    plant_type = { "type_cutting": type_cutting, "type_full": type_full, "type_all": type_all }
    print(plant_type)

    results = listings.search(query) if query else listings.fetch_all()

    print("query:", query)
    print("results:", len(results))

    return render_template("search.html", query=query, city=city, plant_type=plant_type, results=results)

