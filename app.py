from flask import Flask
from flask import render_template, request, redirect, session, abort, make_response
import db, users, config
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
    return render_template("user.html", user=user)

# add profile image
@app.route("/add_image", methods=["GET", "POST"])
def add_image():
    # require_login()

    if request.method == "GET":
        return render_template("add_image.html")

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
@app.route("/image/<int:user_id>")
def show_image(user_id):
    image = users.get_image(user_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

