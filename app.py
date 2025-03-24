from flask import Flask
from flask import render_template, request, redirect, session, abort, make_response
import db, users, config, listings
import sqlite3

app = Flask(__name__)
app.secret_key = config.secret_key

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
            session["user_id"] = user_id
            session["username"] = username
            print("logged in as", username)
            return redirect("/")
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
    if request.method == "GET":
        result = db.query("SELECT username FROM users")

        print("käyttäjät tietokannassa:")
        for user in result:
            print(user["username"])
        
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        city = request.form["city"]

        if password1 != password2:
            return render_template("salasanat eivät täsmää")

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

    if not user:
        abort(404)
    
    listings = users.get_listings(user_id)
    return render_template("user.html", user=user, listings=listings)

# add profile image
@app.route("/add_profile_image", methods=["GET", "POST"])
def add_image():
    # require_login()

    if request.method == "GET":
        return render_template("add_profile_image.html")

    if request.method == "POST":
        # check_csrf()

        file = request.files["image"]
        if not file.filename.endswith(".jpg"):
            # return redirect("/add_image")
            return("ei jpg-tiedosto")

        image = file.read()
        if len(image) > 100 * 1024:
            # return redirect("/add_image")
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
    # require login

    if request.method == "GET":
        return render_template("new_listing.html")
    
    if request.method == "POST":
        name = request.form["name"]
        user_id = session["user_id"]

        try:
            listings.create_listing(name, user_id)
            print("added listing for user", user_id)

            listing = users.newest_listing(user_id)
            session["editing_listing"] = listing
            return redirect("/add_listing_image")
        except:
            return "jotain meni vikaan"

# add listing image
@app.route("/add_listing_image", methods=["GET", "POST"])
def add_listing_image():
    # require_login()

    if request.method == "GET":
        listing = listings.get_listing(session["editing_listing"])
        return render_template("add_listing_image.html", listing=listing)

    if request.method == "POST":
        # check_csrf()

        file = request.files["image"]
        if not file.filename.endswith(".jpg"):
            # return redirect("/add_image")
            return("ei jpg-tiedosto")

        image = file.read()
        if len(image) > 200 * 1024:
            # return redirect("/add_image")
            return("tiedosto on liian suuri")

        listing_id = session["editing_listing"]
        listings.update_image(listing_id, image)
        del session["editing_listing"]
        return redirect("/listing/" + str(listing_id))
    
# listing page
@app.route("/listing/<int:listing_id>")
def show_listing(listing_id):
    listing = listings.get_listing(listing_id)

    if not listing:
        abort(404)
    
    #listings = users.get_listings(user_id)
    return render_template("listing.html", listing=listing, comments=[])

# fetch listing image
@app.route("/image/listing/<int:listing_id>")
def show_listing_image(listing_id):
    image = listings.get_image(listing_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response