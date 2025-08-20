from flask import Flask
from flask import render_template, request, redirect, session, abort, make_response, flash, g
import users, config, listings, comments, images
import sqlite3, secrets, markupsafe, time, math
from utils import form_validation, date_formatter

app = Flask(__name__)
app.secret_key = config.secret_key

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response

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
@app.route("/<int:page>")
def index(page=1):
    page_size = 10
    listing_count = listings.listing_count()
    page_count = math.ceil(listing_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))
    
    first_listing_number = page_size*(page-1)+1

    if page < page_count:
        last_listing_number = first_listing_number + (page_size-1)
    else:
        last_listing_number = first_listing_number + (listing_count%page_size) - 1
    
    all_listings = listings.get_listings_by_page(page, page_size)
    formatted_listings = []

    for listing in all_listings:
        formatted_listing = {
            "listing_id": listing["listing_id"],
            "name": listing["name"],
            "date": date_formatter.format_date(listing["date"]),
            "has_image": listing["has_image"],
            "username": listing["username"],
            "user_id": listing["user_id"],
            "city": listing["city"]
        }
        formatted_listings.append(formatted_listing)

    return render_template("index.html", listings=formatted_listings, page=page, page_count=page_count, first_listing_number=first_listing_number, last_listing_number=last_listing_number, total_count=listing_count)

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

            if active:
                session["user_id"] = user_id
                session["username"] = username
                session["csrf_token"] = secrets.token_hex(16)
                return redirect("/")
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
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    restrictions = form_validation.registration_restrictions
    hint_text = form_validation.form_hint_text

    if request.method == "GET":
        return render_template("register.html", restrictions=restrictions, hint_text=hint_text, filled={})
    
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        city = request.form["city"]

        filled = { "username": username, "city": city }

        if password1 != password2:
            flash("Salasanat eivät täsmää")
            return render_template("register.html", restrictions=restrictions, hint_text=hint_text, filled=filled)

        username_valid, username_error_message = form_validation.validate_username(username)

        if not username_valid:
            flash(username_error_message)
            return render_template("register.html", restrictions=restrictions, hint_text=hint_text, filled=filled)
        
        password_valid, password_error_message = form_validation.validate_password(password1)

        if not password_valid:
            flash(password_error_message)
            return render_template("register.html", restrictions=restrictions, hint_text=hint_text, filled=filled)
        
        city_valid, city_error_message = form_validation.validate_city(city)

        if not city_valid:
            flash(city_error_message)
            return render_template("register.html", restrictions=restrictions, hint_text=hint_text, filled=filled)
        
        try:
            users.create_user(username, password1, city)
            flash("Tunnuksen luonti onnistui. Voit nyt kirjautua sisään.")
            return redirect("/login")
        except sqlite3.IntegrityError:
            filled = { "city": city }
            flash("Käyttäjätunnus varattu")
            return render_template("register.html", restrictions=restrictions, hint_text=hint_text, filled=filled)

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

    if request.method == "GET":
        filled = { "username": user["username"], "city": user["city"] }
        return render_template("edit_profile.html", user=user, restrictions=restrictions, hint_text=hint_text, filled=filled)

    if request.method == "POST":
        check_csrf()
        new_username = request.form["new_username"]
        new_city = request.form["new_city"]

        filled = { "username": new_username, "city": new_city }

        username_valid, username_error_message = form_validation.validate_username(new_username)

        if not username_valid:
            flash(username_error_message)
            return render_template("edit_profile.html", user=user, restrictions=restrictions, hint_text=hint_text, filled=filled)
        
        city_valid, city_error_message = form_validation.validate_city(new_city)

        if not city_valid:
            flash(city_error_message)
            return render_template("edit_profile.html", user=user, restrictions=restrictions, hint_text=hint_text, filled=filled)
        
        try:
            users.update_user(user_id, new_username, new_city)
            flash("Muutokset tallennettu")
            session["username"] = new_username
            filled = { "username": new_username, "city": new_city }
            return render_template("edit_profile.html", user=user, restrictions=restrictions, hint_text=hint_text, filled=filled)
        except sqlite3.IntegrityError:
            flash("Käyttäjätunnus varattu")
            return render_template("edit_profile.html", user=user, restrictions=restrictions, hint_text=hint_text, filled=filled)

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

    if request.method == "POST":
        new_password1 = request.form["new_password1"]
        new_password2 = request.form["new_password2"]
        old_password = request.form["old_password"]

        filled = { "username": user["username"], "city": user["city"] }

        password_correct = users.check_login(user["username"], old_password)

        if not password_correct:
            flash("Väärä salasana")
            return render_template("edit_profile.html", user=user, restrictions=restrictions, hint_text=hint_text, filled=filled)

        if new_password1 != new_password2:
            flash("Salasanat eivät täsmää")
            return render_template("edit_profile.html", user=user, restrictions=restrictions, hint_text=hint_text, filled=filled)

        new_password_valid, new_password_error_message = form_validation.validate_password(new_password1)

        if not new_password_valid:
            flash(new_password_error_message)
            return render_template("edit_profile.html", user=user, restrictions=restrictions, hint_text=hint_text, filled=filled)
        
        if old_password == new_password1:
            flash("Uusi salasana ei voi olla sama kuin vanha salasana")
            return render_template("edit_profile.html", user=user, restrictions=restrictions, hint_text=hint_text, filled=filled)

        users.change_password(user_id, new_password1)
        flash("Salasana vaihdettu")
        return render_template("edit_profile.html", user=user, restrictions=restrictions, hint_text=hint_text, filled=filled)
        
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
            users.remove_image(user_id)
        return redirect("/user/" + str(user_id))


# add listing
@app.route("/new_listing", methods=["GET", "POST"])
def new_listing():
    require_login()
    restrictions = form_validation.new_listing_restrictions
    all_classes = listings.get_all_classes()

    if request.method == "GET":
        return render_template("new_listing.html", restrictions=restrictions, classes=all_classes)
    
    if request.method == "POST":
        check_csrf()
        name = request.form["name"]
        info = request.form["info"]
        user_id = session["user_id"]

        if info.strip() == "":
            info = ""
                
        if not name or len(name) > restrictions["max_name"]:
            abort(403)

        if len(info) > restrictions["max_info"]:
            abort(403)

        classes = request.form.getlist("cutting") + request.form.getlist("classes")        
        listing_classes = []

        for entry in classes:
            if entry:
                option_title, option_value = entry.split(":")

                if option_title not in all_classes:
                    abort(403)
                elif option_value not in all_classes[option_title]:
                    abort(403)

                listing_classes.append((option_title, option_value))

        try:
            listings.create_listing(name, user_id, info, listing_classes)
            listing = users.newest_listing(user_id)
            return redirect("/add_listing_image/" + str(listing))
        except:
            return "Tapahtui virhe"

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

        images.add_image(image, user_id)
        image_id = images.newest_image_from_user(user_id)
        listings.update_image(listing_id, image_id)
        flash("Kuvan lisääminen onnistui")
        return redirect("/listing/" + str(listing_id))
    
# remove listing image
@app.route("/remove/listing_image/<int:listing_id>", methods=["GET", "POST"])
def remove_listing_image(listing_id):
    require_login()
    listing = listings.get_listing(listing_id)

    if not listing:
        abort(404)
        
    if listing["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_listing_image.html", listing=listing)

    if request.method == "POST":
        check_csrf()

        if "continue" in request.form:
            image_id = listing["image_id"]            
            images.remove_image(image_id)
            listings.remove_image(listing_id)
            flash("Kuva poistettiin")
        return redirect("/listing/" + str(listing_id))
    
# listing page
@app.route("/listing/<int:listing_id>")
def show_listing(listing_id):
    listing = listings.get_listing(listing_id)

    if not listing:
        abort(404)

    classes = listings.get_classes(listing_id)
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
                       "user_has_image": comment["user_has_image"]}
        
        if comment["edited_date"]:
            formatted_comment["edited_date"] = date_formatter.format_date_time(comment["edited_date"])
        
        formatted_comments.append(formatted_comment)
    return render_template("listing.html", listing=listing, user=user, comments=formatted_comments, date_added=date_added, restrictions=restrictions, hint_text=hint_text, classes=classes)

# fetch listing image
@app.route("/image/listing/<int:listing_id>")
def show_listing_image(listing_id):
    image_id = listings.get_image_id(listing_id)
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

    class_data = listings.get_classes(listing_id)
    all_classes = listings.get_all_classes()

    listing_classes = {}

    for option_title, option_value in class_data:
        listing_classes[option_title] = option_value

    if request.method == "GET":
        restrictions = form_validation.new_listing_restrictions
        return render_template("edit_listing.html", listing=listing, restrictions=restrictions, hint_text=hint_text, all_classes=all_classes, listing_classes=listing_classes)

    if request.method == "POST":
        check_csrf()
        name = request.form["name"]
        info = request.form["info"]

        if info.strip() == "":
            info = ""

        new_classes = request.form.getlist("cutting") + request.form.getlist("classes")
        updated_classes = []

        for entry in new_classes:
            if entry:
                option_title, option_value = entry.split(":")

                if option_title not in all_classes:
                    abort(403)
                elif option_value not in all_classes[option_title]:
                    abort(403)

                updated_classes.append((option_title, option_value))

        listings.update_listing(listing["id"], name, info, updated_classes)
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
            images.remove_image(listing["image_id"])
            flash("Ilmoitus poistettiin")
        return redirect("/")
    
# add comment to listing
@app.route("/new_comment", methods=["POST"])
def new_comment():
    check_csrf()
    require_login()
    
    if request.method == "POST":
        content = request.form["content"]
        user_id = str(session["user_id"])
        listing_id = request.form["listing_id"]

        content_valid, content_error_message = form_validation.validate_comment(content)

        if not content_valid:
            flash(content_error_message)
            return redirect("/listing/" + str(listing_id)) 
               
        try:
            comments.create_comment(user_id, listing_id, content)
            return redirect("/listing/" + str(listing_id))
        except sqlite3.IntegrityError:
            abort(403)
        except:
            return "Tapahtui virhe"
        
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

        content_valid, content_error_message = form_validation.validate_comment(content)

        if not content_valid:
            flash(content_error_message)
            return redirect("/edit/comment/" + str(comment["listing_id"])) 
               
        comments.update_comment(comment_id, content)
        flash("Muokkaus onnistui")
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

            if user["has_image"]:
                images.remove_image(user["image_id"])

            logout()
            return redirect("/")
        return redirect("/user/" + str(user_id))
    
@app.route("/search")
def search():
    query = request.args.get("query") if request.args.get("query") else ""
    city = request.args.get("city") if request.args.get("city") else ""
    results = listings.search(query, city) if query or city else []

    if results:
        formatted_results = []

        for result in results:
            formatted_result = {
                "result_id": result["listing_id"],
                "name": result["name"],
                "date": date_formatter.format_date(result["date"]),
                "has_image": result["has_image"],
                "username": result["username"],
                "user_id": result["user_id"],
                "city": result["city"]
            }
            formatted_results.append(formatted_result)

    return render_template("search.html", query=query, city=city, results=results)

