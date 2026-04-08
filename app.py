from flask import Flask, render_template, request, redirect, session
import mysql.connector
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.secret_key = "supersecretkey"
bcrypt = Bcrypt(app)

# DB connection
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Write your password here dumbass",
        database="hotel_reservation"
    )

@app.route("/")
def home():
    return render_template("index.html")

# -------------------------
# REGISTER ROUTE
# -------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    next_page = request.args.get("next")   # ✅ ADD THIS LINE

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        db = get_db()
        cursor = db.cursor()

        try:
            query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, hashed_password))
            db.commit()
        except:
            return "Email already exists ❌"

        cursor.close()
        db.close()

        return redirect(f"/login?next={next_page}")   # ✅ NOW THIS WORKS

    return render_template("register.html", next=next_page)   # ✅ pass next

# -------------------------
# LOGIN ROUTE
# -------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    next_page = request.args.get("next")

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        next_page = request.form.get("next")

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user and bcrypt.check_password_hash(user["password"], password):
            session["user_id"] = user["user_id"]
            session["user_name"] = user["name"]
            session.permanent = False

            return redirect(next_page or "/dashboard")   # ✅ FIX HERE
        else:
            return "Invalid email or password ❌"

    return render_template("login.html", next=next_page)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.context_processor
def inject_user():
    return dict(user=session.get("user_name"))

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

    return render_template("dashboard.html", name=session["user_name"], hotels=hotels)

@app.route("/rooms/<int:hotel_id>")
def rooms(hotel_id):

    db = get_db()
    cursor = db.cursor(dictionary=True)

    query = "SELECT * FROM rooms WHERE hotel_id = %s"
    cursor.execute(query, (hotel_id,))
    rooms = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("rooms.html", rooms=rooms, hotel_id=hotel_id)

@app.route("/book/<int:room_id>")
def book(room_id):
    if "user_id" not in session:
        return redirect(f"/login?next=/book/{room_id}")   # 🔥 FORCE LOGIN

    db = get_db()
    cursor = db.cursor()

    user_id = session["user_id"]

    query = """
        INSERT INTO bookings (booking_date, check_in, check_out, status, user_id, room_id)
        VALUES (CURDATE(), CURDATE(), DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'confirmed', %s, %s)
    """
    cursor.execute(query, (user_id, room_id))

    cursor.execute("UPDATE rooms SET availability = 'booked' WHERE room_id = %s", (room_id,))

    db.commit()
    cursor.close()
    db.close()

    return "Room booked successfully! 🎉 <br><a href='/dashboard'>Go to Dashboard</a>"

@app.route("/my_bookings")
def my_bookings():
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT b.booking_id, b.check_in, b.check_out, b.status,
               r.room_type, h.hotel_name
        FROM bookings b
        JOIN rooms r ON b.room_id = r.room_id
        JOIN hotels h ON r.hotel_id = h.hotel_id
        WHERE b.user_id = %s
    """

    cursor.execute(query, (session["user_id"],))
    bookings = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("my_bookings.html", bookings=bookings)

@app.route("/view_hotels")
def view_hotels():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM hotels")
    hotels = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("view_hotels.html", hotels=hotels)

@app.route("/about")
def about():
    return "<h2>About Page</h2>"

@app.route("/help")
def help():
    return "<h2>Help Page</h2>"

@app.route("/contact")
def contact():
    return "<h2>Contact Us Page</h2>"

@app.route("/cancel_booking/<int:booking_id>")
def cancel_booking(booking_id):
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor()

    # 🔐 Only allow user to cancel THEIR booking
    cursor.execute(
        "SELECT room_id FROM bookings WHERE booking_id = %s AND user_id = %s",
        (booking_id, session["user_id"])
    )
    result = cursor.fetchone()

    if result:
        room_id = result[0]

        # Cancel booking
        cursor.execute(
            "UPDATE bookings SET status = 'cancelled' WHERE booking_id = %s",
            (booking_id,)
        )

        # Make room available again
        cursor.execute(
            "UPDATE rooms SET availability = 'available' WHERE room_id = %s",
            (room_id,)
        )

        db.commit()

    cursor.close()
    db.close()

    return redirect("/my_bookings")

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email = %s AND role = 'admin'", (email,))
        admin = cursor.fetchone()

        cursor.close()
        db.close()

        if admin and bcrypt.check_password_hash(admin["password"], password):
            session["admin_id"] = admin["user_id"]
            session["admin_name"] = admin["name"]

            return redirect("/admin_dashboard")
        else:
            return "Invalid Admin Credentials ❌"

    return render_template("admin_login.html")

@app.route("/admin_dashboard")
def admin_dashboard():
    if "admin_id" not in session:
        return redirect("/admin_login")

    return render_template("admin_dashboard.html", name=session["admin_name"])

@app.route("/add_hotel", methods=["GET", "POST"])
def add_hotel():
    if "admin_id" not in session:
        return redirect("/admin_login")

    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"]
        description = request.form["description"]

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO hotels (hotel_name, location, description) VALUES (%s, %s, %s)",
            (name, location, description)
        )

        db.commit()
        cursor.close()
        db.close()

        return redirect("/admin_dashboard")

    return render_template("add_hotel.html")

@app.route("/add_room", methods=["GET", "POST"])
def add_room():
    if "admin_id" not in session:
        return redirect("/admin_login")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM hotels")
    hotels = cursor.fetchall()

    if request.method == "POST":
        room_type = request.form["room_type"]
        price = request.form["price"]
        hotel_id = request.form["hotel_id"]

        cursor.execute(
            "INSERT INTO rooms (room_type, price, availability, hotel_id) VALUES (%s, %s, 'available', %s)",
            (room_type, price, hotel_id)
        )

        db.commit()
        cursor.close()
        db.close()

        return redirect("/admin_dashboard")

    return render_template("add_room.html", hotels=hotels)

@app.route("/admin_bookings")
def admin_bookings():
    if "admin_id" not in session:
        return redirect("/admin_login")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT b.booking_id, b.status, b.check_in, b.check_out,
               u.name AS user_name, u.email,
               h.hotel_name, r.room_type
        FROM bookings b
        JOIN users u ON b.user_id = u.user_id
        JOIN rooms r ON b.room_id = r.room_id
        JOIN hotels h ON r.hotel_id = h.hotel_id
    """

    cursor.execute(query)
    bookings = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("admin_bookings.html", bookings=bookings)

@app.route("/delete_booking/<int:booking_id>")
def delete_booking(booking_id):
    if "admin_id" not in session:
        return redirect("/admin_login")

    db = get_db()
    cursor = db.cursor()

    # get room id first
    cursor.execute("SELECT room_id FROM bookings WHERE booking_id = %s", (booking_id,))
    result = cursor.fetchone()

    if result:
        room_id = result[0]

        # delete booking
        cursor.execute("DELETE FROM bookings WHERE booking_id = %s", (booking_id,))

        # make room available again
        cursor.execute("UPDATE rooms SET availability='available' WHERE room_id=%s", (room_id,))

        db.commit()

    cursor.close()
    db.close()

    return redirect("/admin_bookings")

@app.route("/admin_hotels")
def admin_hotels():
    if "admin_id" not in session:
        return redirect("/admin_login")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM hotels")
    hotels = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("admin_hotels.html", hotels=hotels)

@app.route("/delete_hotel/<int:hotel_id>")
def delete_hotel(hotel_id):
    if "admin_id" not in session:
        return redirect("/admin_login")

    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM hotels WHERE hotel_id = %s", (hotel_id,))
    db.commit()

    cursor.close()
    db.close()

    return redirect("/admin_hotels")

if __name__ == "__main__":
    app.run(debug=True)
