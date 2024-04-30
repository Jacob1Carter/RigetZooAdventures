import os
import json
import requests

from flask import Flask, render_template, request, session, url_for, redirect
from functools import wraps
from sqlalchemy.orm.attributes import flag_modified

from flask_session import Session
from datetime import datetime

from models import User, Ticket, Animal, UserFeedback
from database import db, hash_password, validate_email

#   initialize app and database

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_pyfile("config.py")
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data", "database.py")

Session(app)
db.init_app(app)


#   Login/Session/Admin checks


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("id"):
            return redirect(url_for("login"))
        else:
            return func(*args, **kwargs)

    return wrapper


def session_check():
    if not session.get("id"):
        return False
    else:
        return True


def admin_check():
    if session_check():
        user = User.query.filter_by(id=session["id"]).first()
        if user:
            if user.is_admin:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def member_check():
    if session_check():
        user = User.query.filter_by(id=session["id"]).first()
        if user:
            if user.is_member:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


#   Routes

#   Main pages


@app.route("/")
def landing():
    is_session = session_check()
    is_admin = admin_check()

    page_data = json.load(open("data/pages/landing.json"))
    site_vars = {"alerts": [], "is_session": is_session, "is_admin": is_admin}
    return render_template("main/landing.html", page_data=page_data, site_vars=site_vars)


@app.route("/about-us")
def about_us():
    is_session = session_check()
    is_admin = admin_check()

    page_data = json.load(open("data/pages/about-us.json"))
    site_vars = {"alerts": [], "is_session": is_session, "is_admin": is_admin}
    return render_template("main/info-page-template.html", page_data=page_data, site_vars=site_vars)


@app.route("/emergency-information")
def emergency_information():
    is_session = session_check()
    is_admin = admin_check()

    page_data = json.load(open("data/pages/emergency-information.json"))
    site_vars = {"alerts": [], "is_session": is_session, "is_admin": is_admin}
    return render_template("main/info-page-template.html", page_data=page_data, site_vars=site_vars)


@app.route("/legal-information")
def legal_information():
    is_session = session_check()
    is_admin = admin_check()

    page_data = json.load(open("data/pages/legal-information.json"))
    site_vars = {"alerts": [], "is_session": is_session, "is_admin": is_admin}
    return render_template("main/info-page-template.html", page_data=page_data, site_vars=site_vars)


@app.route("/facilities")
def facilities():
    is_session = session_check()
    is_admin = admin_check()

    page_data = json.load(open("data/pages/facilities.json"))
    site_vars = {"alerts": [], "is_session": is_session, "is_admin": is_admin}
    return render_template("main/info-page-template.html", page_data=page_data, site_vars=site_vars)


@app.route("/location")
def location():
    is_session = session_check()
    is_admin = admin_check()
    page_data = json.load(open("data/pages/location.json"))
    site_vars = {"alerts": [], "is_session": is_session, "is_admin": is_admin}

    return render_template("main/location.html", page_data=page_data, site_vars=site_vars)


@app.route("/map")
def map_page():
    is_session = session_check()
    is_admin = admin_check()

    page_data = json.load(open("data/pages/map.json"))
    site_vars = {"alerts": [], "is_session": is_session, "is_admin": is_admin}
    return render_template("main/map.html", page_data=page_data, site_vars=site_vars)


@app.route("/contact-us", methods=["GET", "POST"])
def contact_us():
    is_session = session_check()
    is_admin = admin_check()
    site_vars = {"alerts": [], "is_session": is_session, "is_admin": is_admin}

    if request.method == "POST":
        if request.args.get("type") == "a":
            text = request.form.get("anonymous-input")

            feedback = UserFeedback(question="anonymous feedback", answer=text)
            db.session.add(feedback)
            db.session.commit()
        elif request.args.get("type") == "d":
            text = request.form.get("direct-input")
            return_email = request.form.get("email")
            if not return_email or return_email == "":
                if is_session:
                    user = User.query.filter_by(id=session.get("id")).first()
                    return_email = user.email
                else:
                    return_email = False
                    site_vars["alerts"].append({"type": "danger", "text": "An error occurred"})

            if return_email:
                feedback = UserFeedback(question=f"Contact from: {return_email}", answer=text)
                db.session.add(feedback)
                db.session.commit()
        else:
            site_vars["alerts"].append({"type": "danger", "text": "An error occurred"})
    return render_template("main/contact-us.html", title="RZA - Contact us", site_vars=site_vars)


@app.route("/search-animals", methods=["GET", "POST"])
def search_animals():
    is_session = session_check()
    is_admin = admin_check()
    site_vars = {"alerts": [], "is_session": is_session, "is_admin": is_admin}

    search_request = request.args.get("search")
    if search_request and search_request != "":
        title = f"Results for: {search_request}"
        search_filter = f"%{search_request}%"
        animal_search = Animal.query.filter(Animal.species_name.like(search_filter)).all()
    else:
        title = "Search animals"
        animal_search = Animal.query.union_all()

    if request.method == "POST":
        search = request.form.get("search")
        if search != "":
            return redirect(f"/search-animals?search={search}")

    return render_template(
        "main/search-animals.html", title=title, site_vars=site_vars, animals=animal_search
    )


@app.route("/view-animal/<code>")
def view_animal(code):
    is_session = session_check()
    is_admin = admin_check()

    date_today = datetime.utcnow().date()
    animal = Animal.query.filter_by(id=code).first()
    for i in animal.individual_details:
        birth_date = animal.individual_details[i]["birth_date"]
        date_obj = datetime(int(birth_date[:4]), int(birth_date[4:6]), int(birth_date[6:8])).date()
        age = int(int(str(date_today - date_obj)[:4])/365)
        animal.individual_details[i]["age"] = age

    api_key = "qESvmw06J9jtQtvq1hBb8A==FGYGbOnv5xI2nIAE"
    api_url = f"https://api.api-ninjas.com/v1/animals?name={animal.api_name}"
    api_request = requests.get(api_url, headers={'X-Api-Key': api_key})
    api_data = {"name": "error"}
    if api_request.status_code == requests.codes.ok:
        response = api_request.json()
        for animal_data in response:
            if animal_data["name"].lower() == animal.api_name.lower() or \
                    animal_data["name"].lower() == animal.species_name.lower():
                api_data = animal_data
        if api_data == {"name": "error"}:
            api_data = response[0]

    site_vars = {"alerts": [], "is_session": is_session, "is_admin": is_admin}
    return render_template("main/view-animal.html", title=f"{animal.species_name}",
                           site_vars=site_vars, animal=animal, api_data=api_data)


#   Login/register pages


@app.route("/login", methods=["GET", "POST"])
def login():
    site_vars = {"alerts": []}

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        with app.app_context():
            db.create_all()
            user = User.query.filter_by(email=email).first()
            if user:
                if hash_password(password) == user.password_md5:
                    session["id"] = user.id
                    return redirect(url_for("landing"))
                else:
                    site_vars["alerts"].append({"type": "danger", "text": "Incorrect email or password"})
            else:
                site_vars["alerts"].append({"type": "danger", "text": "Incorrect email or password"})
    return render_template("user/login.html", title="RZA - login", site_vars=site_vars)


@app.route("/register", methods=["GET", "POST"])
def register():
    site_vars = {"alerts": []}

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        with app.app_context():
            db.create_all()
            user = User.query.filter_by(email=email).first()
            if user:
                site_vars["alerts"].append({"type": "danger", "text": "Email already in use"})
            else:
                if validate_email(email):
                    password_md5 = hash_password(password)
                    confirm_password_md5 = hash_password(confirm_password)
                    if password_md5 == confirm_password_md5:
                        new_user = User(email=email, password_md5=password_md5)
                        feedback = request.form.get("feedback")
                        if feedback and feedback != "":
                            new_feedback = UserFeedback(question="How did you hear about us?", answer=feedback)
                            db.session.add(new_feedback)
                        db.session.add(new_user)
                        db.session.commit()

                        session["id"] = new_user.id
                        return redirect(url_for("landing"))
                    else:
                        site_vars["alerts"].append({"type": "danger", "text": "Passwords must match"})
                else:
                    site_vars["alerts"].append({"type": "danger", "text": "Invalid email"})
    return render_template("user/register.html", title="RZA - register", site_vars=site_vars)


#   User pages


@app.route("/profile")
@login_required
def profile():
    is_admin = admin_check()
    site_vars = {"alerts": [], "is_session": True, "is_admin": is_admin}

    user = User.query.filter_by(id=session.get("id")).first()
    return render_template("user/profile.html", title="Your profile", site_vars=site_vars, user=user)


@app.route("/settings")
@login_required
def settings():
    is_admin = admin_check()

    site_vars = {"alerts": [], "is_session": True, "is_admin": is_admin}
    return render_template("user/settings.html", title="Settings", site_vars=site_vars)


@app.route("/membership", methods=["GET", "POST"])
@login_required
def membership():
    is_admin = admin_check()
    page_data = json.load(open("data/pages/membership.json"))
    site_vars = {"alerts": [], "is_session": True, "is_admin": is_admin}

    if request.method == "POST":
        if True:  # this is where payment would occur
            user = User.query.filter_by(id=session.get("id")).first()

            user.is_member = True
            db.session.commit()

            return redirect("/profile")
        else:
            site_vars["alerts"].append({"type": "danger", "text": "Payment failed"})

    return render_template("user/membership.html", page_data=page_data, site_vars=site_vars)


@app.route("/tickets", methods=["GET", "POST"])
@login_required
def tickets():
    is_admin = admin_check()
    is_member = member_check()
    site_vars = {"alerts": [], "is_session": True, "is_admin": is_admin, "is_member": is_member}

    if request.method == "POST":
        if request.args.get("type") == "r":
            date = request.form.get("date_r")

            cost = {
                "adult": 5.0,
                "child": 2.0,
                "student": 3.50
            }
            admit = {}
            total_cost = 0

            for ticket_type in cost:
                value = request.form.get(ticket_type)
                if int(value) > 0:
                    admit.update({ticket_type: value})
                    total_cost += cost[ticket_type]

            if is_member:
                total_cost = round(total_cost * 0.8, 2)

            cart_ticket = {
                "type": "r",
                "admit": admit,
                "cost": total_cost,
                "date": date,
                "rooms": ""
            }
            if not session.get("cart"):
                session["cart"] = []
                session["cart"].append(cart_ticket)
            else:
                session["cart"].append(cart_ticket)
            session.modified = True
            redirect_endpoint = request.form.get("redirect")
            return redirect(redirect_endpoint)
        elif request.args.get("type") == "e":
            date = request.form.get("date_e")

            admit = {}

            for ticket_type in ["supervisors", "students"]:
                value = request.form.get(ticket_type)
                if int(value) > 0:
                    admit.update({ticket_type: value})

            cart_ticket = {
                "type": "e",
                "admit": admit,
                "date": date,
                "cost": 30.0,
                "rooms": ""
            }
            if not session.get("cart"):
                session["cart"] = []
                session["cart"].append(cart_ticket)
            else:
                session["cart"].append(cart_ticket)
            session.modified = True
            redirect_endpoint = request.form.get("redirect")
            return redirect(redirect_endpoint)
        else:
            site_vars["alerts"].append({"type": "danger", "text": "An error occurred"})

    date_today = datetime.utcnow().date()
    return render_template("user/order-ticket.html", title="Buy a ticket", site_vars=site_vars, date_today=date_today)


@app.route("/book-room", methods=["GET", "POST"])
@login_required
def book_room():
    is_admin = admin_check()
    is_member = member_check()
    site_vars = {"alerts": [], "is_session": True, "is_admin": is_admin, "is_member": is_member}

    rooms = []
    for i in range(0, 10):
        rooms.append({"Availability": "available", "cost": 15.0, "capacity": 4})

    if request.method == "POST":
        cost = 0
        rooms_str = ""
        for i, room in enumerate(rooms):
            if room["Availability"] != "unavailable":
                if request.form.get(str(i + 1)):
                    rooms_str += str(i)
                    cost += rooms[i]["cost"]

        if is_member:
            cost = round(cost * 0.8, 2)

        session["cart"][-1]["rooms"] = rooms_str
        session["cart"][-1]["cost"] += cost
        session.modified = True
        return redirect("/cart")

    ticket = session.get("cart")[-1]
    date = datetime(int(ticket["date"][:4]), int(ticket["date"][5:7]), int(ticket["date"][8:]))
    other_tickets = Ticket.query.filter_by(date_expires=date)
    for other_ticket in other_tickets:
        for c in other_ticket.hotel_rooms:
            if c.isdigit():
                rooms[int(c)]["Availability"] = "unavailable"

    return render_template("user/order-room.html", title="Book a room", site_vars=site_vars, rooms=rooms)


@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    is_admin = admin_check()
    site_vars = {"alerts": [], "is_session": True, "is_admin": is_admin}

    if request.method == "POST":
        if True:  # this is where payment would occur
            for ticket in session.get("cart"):
                new_ticket = Ticket(
                    ticket_holder_id=session.get("id"),
                    ticket_type=ticket["type"],
                    date_expires=datetime(int(ticket["date"][:4]), int(ticket["date"][5:7]), int(ticket["date"][8:])),
                    admit=ticket["admit"],
                    hotel_rooms=ticket["rooms"],
                    cost=ticket["cost"]
                )

                db.session.add(new_ticket)
            db.session.commit()

            session["cart"] = []
            session.modified = True

            return redirect("/your-tickets")
        else:
            site_vars["alerts"].append({"type": "danger", "text": "Payment failed"})

    pending = session.get("cart")
    if not pending:
        pending = []
    return render_template("user/cart.html", title="Your cart", site_vars=site_vars, pending=pending)


@app.route("/your-tickets")
@login_required
def view_tickets():
    is_admin = admin_check()
    site_vars = {"alerts": [], "is_session": True, "is_admin": is_admin}

    user_tickets = Ticket.query.filter_by(ticket_holder_id=session.get("id")).all()
    for ticket in user_tickets:
        if ticket.date_expires.date() < datetime.utcnow().date():
            user_tickets.pop(ticket)
    return render_template("user/view-tickets.html",
                           title="Your tickets", site_vars=site_vars, user_tickets=user_tickets)


#   Admin pages


@app.route("/admin")
@login_required
def admin_home():
    if admin_check():
        user = User.query.filter_by(id=session["id"]).first()
        return render_template("admin/home.html", email=user.email, title="Admin")
    else:
        return redirect(url_for("landing"))


@app.route("/admin/manage-users", methods=["GET", "POST"])
@login_required
def manage_users():
    if admin_check():
        user = User.query.filter_by(id=session["id"]).first()
        alerts = []

        if request.method == "POST":
            email = request.form.get("email")
            toggle_admin_user = User.query.filter_by(email=email).first()
            if toggle_admin_user:
                if toggle_admin_user.is_admin:
                    toggle_admin_user.is_admin = False
                    alerts.append({
                        "type": "primary",
                        "text": f"User '{toggle_admin_user.email}' is no longer an admin"}
                    )
                else:
                    toggle_admin_user.is_admin = True
                    alerts.append({"type": "primary", "text": f"User '{toggle_admin_user.email}' is now an admin"})
                db.session.add(toggle_admin_user)
                db.session.commit()
            else:
                alerts.append({"type": "danger", "text": f"User '{email}' not found"})

        return render_template("admin/manage-users.html", email=user.email, alerts=alerts, title="Admin")
    else:
        return redirect(url_for("landing"))


@app.route("/admin/manage-images", methods=["GET", "POST"])
@login_required
def manage_images():
    if admin_check():
        user = User.query.filter_by(id=session["id"]).first()

        if request.method == "POST":
            if "new-image" in request.files:
                new_image = request.files["new-image"]
                if new_image.filename != "":
                    new_image.save(f"static/assets/variable-images/{new_image.filename}")

            for file in request.form:
                if os.path.isfile(f"static/assets/variable-images/{file}"):
                    os.remove(f"static/assets/variable-images/{file}")

        image_list = os.listdir("static/assets/variable-images")
        return render_template("admin/manage-images.html", email=user.email, title="Admin", image_list=image_list)
    else:
        return redirect(url_for("landing"))


@app.route("/admin/manage-pages")
@login_required
def manage_pages():
    if admin_check():
        user = User.query.filter_by(id=session["id"]).first()

        pages = os.listdir("data/pages")
        pages_cut = []
        for page in pages:
            page = page[:-5]
            pages_cut.append(page)
        return render_template("admin/manage-pages.html", email=user.email, title="Admin", pages=pages_cut)
    else:
        return redirect(url_for("landing"))


@app.route("/admin/manage-animals")
@login_required
def manage_animals():
    if admin_check():
        user = User.query.filter_by(id=session["id"]).first()
        animals = Animal.query.union_all()
        return render_template("admin/manage-animals.html", email=user.email, title="Admin", animals=animals)
    else:
        return redirect(url_for("landing"))


@app.route("/admin/edit-page/<name>", methods=["GET", "POST"])
@login_required
def edit_page(name):
    if admin_check():
        pages = os.listdir("data/pages")
        if name + ".json" in pages:
            user = User.query.filter_by(id=session["id"]).first()
            page_data = json.load(open(f"data/pages/{name}.json", "r"))

            if request.method == "POST":
                page_name = request.form.get("name")
                heading = request.form.get("heading")

                content = page_data["content"]
                for item in request.form:
                    if item != "name" and item != "heading":
                        value = request.form.get(item)
                        for dic in content:
                            if dic["name"] == item:
                                dic["content"] = value

                if name == "location":
                    api_key = request.form.get("api_key")
                    lat = request.form.get("lat")
                    lng = request.form.get("lng")

                    new_json = {
                        "name": page_name,
                        "heading": heading,
                        "content": content,
                        "map": {"key": api_key, "lat": lat, "lng": lng}
                    }
                else:
                    new_json = {
                        "name": page_name,
                        "heading": heading,
                        "content": content
                    }

                with open(f"data/pages/{name}.json", "w") as f:
                    json.dump(new_json, f)

            page_data = json.load(open(f"data/pages/{name}.json", "r"))
            image_list = os.listdir("static/assets/variable-images")
            return render_template(
                "admin/edit-page.html", page_data=page_data, name=name,
                email=user.email, title="Admin", image_list=image_list)
        else:
            return redirect(url_for("manage_pages"))
    else:
        return redirect(url_for("landing"))


@app.route("/admin/edit-animal/<animal_id>", methods=["GET", "POST"])
@login_required
def edit_animal(animal_id):
    if admin_check():
        if request.method == "POST":
            species_name = request.form.get("species_name")
            api_name = request.form.get("api_name")
            info = request.form.get("info")
            image = request.form.get("image")

            animal = Animal.query.filter_by(id=animal_id).first()

            pop_list = []
            update_list = []
            details = animal.individual_details
            for individual in details:
                name = request.form.get(f"{individual}name")
                species = request.form.get(f"{individual}species")
                gender = request.form.get(f"{individual}gender")
                birth_date = request.form.get(f"{individual}birth_date")
                description = request.form.get(f"{individual}description")
                image = request.form.get(f"{individual}image")

                individual_update = {
                    name: {
                        "species": species,
                        "gender": gender,
                        "birth_date": birth_date,
                        "description": description,
                        "image": image,
                    }
                }

                if individual != name:
                    pop_list.append(individual)
                update_list.append(individual_update)

            for individual in pop_list:
                details.pop(individual)
            for individual in update_list:
                details.update(individual)

            animal.species_name = species_name
            animal.api_name = api_name
            animal.info = info
            animal.image = image

            animal.individual_details = details
            flag_modified(animal, "individual_details")
            db.session.commit()

        user = User.query.filter_by(id=session["id"]).first()
        animal = Animal.query.filter_by(id=animal_id).first()
        image_list = os.listdir("static/assets/variable-images")

        return render_template("admin/edit-animal.html", animal=animal,
                               email=user.email, title="Admin", image_list=image_list)
    else:
        return redirect(url_for("landing"))


@app.route("/admin/add-animal")
@login_required
def add_animal():
    if admin_check():
        user = User.query.filter_by(id=session["id"]).first()
        return render_template("admin/add-animal.html", email=user.email, title="Admin")
    else:
        return redirect(url_for("landing"))


@app.route("/admin/view-stats")
@login_required
def view_stats():
    if admin_check():
        user = User.query.filter_by(id=session["id"]).first()

        all_feedback = UserFeedback.query.union_all()
        return render_template("admin/view-stats.html", email=user.email, title="Admin", all_feedback=all_feedback)
    else:
        return redirect(url_for("landing"))


@app.route("/admin/view-hotel")
@login_required
def view_hotel():
    if admin_check():
        user = User.query.filter_by(id=session["id"]).first()
        return render_template("admin/view-hotel.html", email=user.email, title="Admin")
    else:
        return redirect(url_for("landing"))


#   Tools


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/reset/<code>")
def reset(code):
    if code == "0":
        db.drop_all()
        print("database reset")
    elif code == "1":
        db.drop_all()
        database_preset = json.load(open("data/database-preset.json"))
        with app.app_context():
            db.create_all()
            for user_preset in database_preset["users"]:
                user = User(
                    email=user_preset["email"],
                    password_md5=hash_password(user_preset["password"]),
                    is_member=True if user_preset["is_member"] == "True" else False,
                    is_admin=True if user_preset["is_admin"] == "True" else False
                )
                db.session.add(user)

            for animal_preset in database_preset["animals"]:
                animal = Animal(
                    species_name=animal_preset["species_name"],
                    api_name=animal_preset["api_name"],
                    info=animal_preset["info"],
                    individual_details=animal_preset["individual_details"],
                    image=animal_preset["image"]
                )
                db.session.add(animal)

            db.session.commit()

        print("database reset and remade")

    session.clear()
    return redirect(url_for("landing"))


#   Run


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
