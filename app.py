from flask import Flask, render_template, request, redirect, session
import mysql.connector
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config["SESSION_PERMANENT"] = False

bcrypt = Bcrypt(app)

# Make 'user' available in all templates for the navbar
@app.context_processor
def inject_user():
    return dict(user=session.get("user_name"))

# -------------------------
# DATABASE CONNECTION
# -------------------------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="09082007@a",   # 🔥 PUT YOUR MYSQL PASSWORD
        database="hotel_reservation"
    )

# -------------------------
# HOME
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")

# -------------------------
# REGISTER
# -------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed = bcrypt.generate_password_hash(password).decode("utf-8")

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",
            (name, email, hashed)
        )

        db.commit()
        cursor.close()
        db.close()

        return redirect("/login")

    return render_template("register.html")

# -------------------------
# LOGIN (ADMIN + USER)
# -------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user and bcrypt.check_password_hash(user["password"], password):
            session["user_id"] = user["user_id"]
            session["user_name"] = user["name"]
            session["role"] = user["role"]

            if user["role"] == "admin":
                return redirect("/admin_dashboard")
            else:
                return redirect("/dashboard")

        return "Invalid login ❌"

    return render_template("login.html")

# -------------------------
# LOGOUT
# -------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# -------------------------
# USER DASHBOARD
# -------------------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM hotels")
    hotels = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("dashboard.html", hotels=hotels, name=session.get("user_name"))

# -------------------------
# VIEW HOTELS
# -------------------------
@app.route("/view_hotels")
def view_hotels():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM hotels")
    hotels = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("view_hotels.html", hotels=hotels)

# -------------------------
# VIEW ROOMS
# -------------------------
@app.route("/rooms/<int:hotel_id>")
def rooms(hotel_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM rooms WHERE hotel_id=%s", (hotel_id,))
    rooms = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("rooms.html", rooms=rooms, hotel_id=hotel_id)

# -------------------------
# BOOK ROOM
# -------------------------
@app.route("/book/<int:room_id>")
def book(room_id):
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO bookings (booking_date, check_in, check_out, status, user_id, room_id)
        VALUES (CURDATE(), CURDATE(), DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'confirmed', %s, %s)
    """, (session["user_id"], room_id))

    cursor.execute("UPDATE rooms SET availability='booked' WHERE room_id=%s", (room_id,))

    db.commit()
    cursor.close()
    db.close()

    return redirect("/dashboard")

# -------------------------
# MY BOOKINGS
# -------------------------
@app.route("/my_bookings")
def my_bookings():
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT b.booking_id, r.room_type, h.hotel_name, b.status, b.check_in, b.check_out
        FROM bookings b
        JOIN rooms r ON b.room_id=r.room_id
        JOIN hotels h ON r.hotel_id=h.hotel_id
        WHERE b.user_id=%s
    """, (session["user_id"],))

    bookings = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("my_bookings.html", bookings=bookings)

# -------------------------
# CANCEL BOOKING
# -------------------------
@app.route("/cancel_booking/<int:booking_id>")
def cancel_booking(booking_id):
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT room_id FROM bookings WHERE booking_id=%s", (booking_id,))
    room_id = cursor.fetchone()[0]

    cursor.execute("DELETE FROM bookings WHERE booking_id=%s", (booking_id,))
    cursor.execute("UPDATE rooms SET availability='available' WHERE room_id=%s", (room_id,))

    db.commit()
    cursor.close()
    db.close()

    return redirect("/my_bookings")

# -------------------------
# ADMIN DASHBOARD
# -------------------------
@app.route("/admin_dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect("/login")

    return render_template("admin_dashboard.html", name=session.get("user_name"))

# -------------------------
# ADMIN VIEW BOOKINGS
# -------------------------
@app.route("/admin_bookings")
def admin_bookings():
    if session.get("role") != "admin":
        return redirect("/login")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT b.booking_id, u.name AS user_name, u.email,
               r.room_type, h.hotel_name, b.status
        FROM bookings b
        JOIN users u ON b.user_id=u.user_id
        JOIN rooms r ON b.room_id=r.room_id
        JOIN hotels h ON r.hotel_id=h.hotel_id
    """)

    bookings = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("admin_bookings.html", bookings=bookings)

# -------------------------
# ADMIN HOTELS
# -------------------------
@app.route("/admin_hotels")
def admin_hotels():
    if session.get("role") != "admin":
        return redirect("/login")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM hotels")
    hotels = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("admin_hotels.html", hotels=hotels)

# -------------------------
# DELETE HOTEL
# -------------------------
@app.route("/delete_hotel/<int:hotel_id>")
def delete_hotel(hotel_id):
    if session.get("role") != "admin":
        return redirect("/login")

    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM hotels WHERE hotel_id=%s", (hotel_id,))
    db.commit()

    cursor.close()
    db.close()

    return redirect("/admin_hotels")

# -------------------------
# ADD HOTEL
# -------------------------
@app.route("/add_hotel", methods=["GET","POST"])
def add_hotel():
    if session.get("role") != "admin":
        return redirect("/login")

    if request.method == "POST":
        name = request.form["hotel_name"]
        location = request.form["location"]
        description = request.form.get("description", "")

        db = get_db()
        cursor = db.cursor()

        cursor.execute("INSERT INTO hotels (hotel_name, location, description) VALUES (%s,%s,%s)", (name, location, description))

        db.commit()
        cursor.close()
        db.close()

        return redirect("/admin_dashboard")

    return render_template("add_hotel.html")

# -------------------------
# ADD ROOM
# -------------------------
@app.route("/add_room", methods=["GET","POST"])
def add_room():
    if session.get("role") != "admin":
        return redirect("/login")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        room_type = request.form["room_type"]
        price = request.form["price"]
        hotel_id = request.form["hotel_id"]

        cursor.execute(
            "INSERT INTO rooms (room_type, price, availability, hotel_id) VALUES (%s,%s,'available',%s)",
            (room_type, price, hotel_id)
        )

        db.commit()
        cursor.close()
        db.close()

        return redirect("/admin_dashboard")

    cursor.execute("SELECT * FROM hotels")
    hotels = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("add_room.html", hotels=hotels)

# -------------------------
# DELETE BOOKING (ADMIN)
# -------------------------
@app.route("/delete_booking/<int:booking_id>")
def delete_booking(booking_id):
    if session.get("role") != "admin":
        return redirect("/login")

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT room_id FROM bookings WHERE booking_id=%s", (booking_id,))
    result = cursor.fetchone()
    if result:
        cursor.execute("DELETE FROM bookings WHERE booking_id=%s", (booking_id,))
        cursor.execute("UPDATE rooms SET availability='available' WHERE room_id=%s", (result[0],))

    db.commit()
    cursor.close()
    db.close()

    return redirect("/admin_bookings")

# -------------------------
# ABOUT PAGE
# -------------------------
@app.route("/about")
def about():
    return render_template("about.html")

# -------------------------
# HELP PAGE
# -------------------------
@app.route("/help")
def help_page():
    return render_template("help.html")

# -------------------------
# CONTACT PAGE
# -------------------------
@app.route("/contact")
def contact():
    return render_template("contact.html")

# -------------------------
if __name__ == "__main__":
    app.run(debug=True)