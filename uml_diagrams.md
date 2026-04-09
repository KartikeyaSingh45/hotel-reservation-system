# UML Diagrams — Hotel Reservation System
> All diagrams are based **exclusively** on actual code in [app.py](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py) and [database.sql](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/database.sql).  
> Each image is print-ready. **Right-click any image → Save Image As** to extract it.

---

## 1. Activity Diagram

![Activity Diagram](file:///C:/Users/Kartikeya/.gemini/antigravity/brain/355a4c51-01f5-458e-a986-a72f9c9b6c2b/activity_diagram_1775766945919.png)

### What It Shows
The end-to-end user flow from visiting the homepage to cancelling a booking.

### Every Element Traced to Code

| Diagram Element | Code Reference |
|---|---|
| `Visit Homepage` | `@app.route("/")` → [home()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#36-39) |
| `Logged in?` | `if "user_id" not in session` — checked in [dashboard()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#119-134), [book()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#174-195), [my_bookings()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#199-221), [cancel_booking()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#225-248) |
| `Create Session (user_id, user_name, role)` | `session["user_id"] = user["user_id"]` etc. in [login()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#75-106) |
| `Validate Credentials` | `bcrypt.check_password_hash(user["password"], password)` in [login()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#75-106) |
| `Role == admin?` | `if user["role"] == "admin": return redirect("/admin_dashboard")` in [login()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#75-106) |
| `SELECT * FROM hotels` | `cursor.execute("SELECT * FROM hotels")` in [dashboard()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#119-134) |
| `SELECT * FROM rooms WHERE hotel_id` | `cursor.execute("SELECT * FROM rooms WHERE hotel_id=%s", (hotel_id,))` in [rooms()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#154-170) |
| `Room available?` | `{% if room.availability == 'available' %}` in [rooms.html](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/templates/rooms.html); `availability` field in [rooms](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#154-170) table |
| `INSERT INTO bookings` | In [book()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#174-195): `INSERT INTO bookings (booking_date, check_in, check_out, status, user_id, room_id) VALUES (CURDATE(), CURDATE(), DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'confirmed', %s, %s)` |
| `UPDATE rooms SET availability='booked'` | In [book()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#174-195): `cursor.execute("UPDATE rooms SET availability='booked' WHERE room_id=%s", (room_id,))` |
| `Flash "Room booked!"` | `flash("Room booked successfully! 🎉", "success")` in [book()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#174-195) |
| `DELETE FROM bookings` | In [cancel_booking()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#225-248): `cursor.execute("DELETE FROM bookings WHERE booking_id=%s", ...)` |
| `UPDATE rooms SET availability='available'` | In [cancel_booking()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#225-248): `cursor.execute("UPDATE rooms SET availability='available' WHERE room_id=%s", ...)` |

---

## 2. Class Diagram

![Class Diagram](file:///C:/Users/Kartikeya/.gemini/antigravity/brain/355a4c51-01f5-458e-a986-a72f9c9b6c2b/class_diagram_1775766960848.png)

### What It Shows
The 4 database entities, their attributes, and relationships. Each class = one MySQL table.

### Every Attribute Traced to Code

**User** (table: `users`)

| Attribute | Defined in | Used in |
|---|---|---|
| `user_id` INT PK | [database.sql](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/database.sql) line 12, AUTO_INCREMENT | `session["user_id"]`, `bookings.user_id` FK, `WHERE b.user_id=%s` |
| `name` VARCHAR(100) | [database.sql](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/database.sql) line 13 | `session["user_name"] = user["name"]`, shown in [dashboard.html](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/templates/dashboard.html) as `{{ name }}` |
| `email` VARCHAR(100) UNIQUE | [database.sql](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/database.sql) line 14 | [login()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#75-106): `WHERE email=%s`, shown in [admin_bookings.html](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/templates/admin_bookings.html) |
| `password` VARCHAR(255) | [database.sql](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/database.sql) line 15 | `bcrypt.generate_password_hash()` on register, `bcrypt.check_password_hash()` on login |
| `role` VARCHAR(20) = 'customer' | [database.sql](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/database.sql) line 16 | `session["role"] = user["role"]`, `if session.get("role") != "admin"` in all admin routes |
| `created_at` TIMESTAMP | [database.sql](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/database.sql) line 17 | stored automatically, not displayed in UI |

**Hotel** (table: [hotels](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#138-150))

| Attribute | Defined in | Used in |
|---|---|---|
| `hotel_id` INT PK | [database.sql](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/database.sql) line 24 | `rooms.hotel_id` FK, `WHERE hotel_id=%s` in [rooms()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#154-170), `/rooms/{{ hotel.hotel_id }}` in templates |
| `hotel_name` VARCHAR(150) | [database.sql](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/database.sql) line 25 | `request.form["hotel_name"]` in [add_hotel()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#351-374), shown in [dashboard.html](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/templates/dashboard.html), [view_hotels.html](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/templates/view_hotels.html), [admin_bookings.html](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/templates/admin_bookings.html) |
| `location` VARCHAR(200) | [database.sql](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/database.sql) line 26 | `request.form["location"]` in [add_hotel()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#351-374), shown in hotel cards |
| `description` TEXT | [database.sql](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/database.sql) line 27 | `request.form.get("description","")` in [add_hotel()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#351-374), shown in hotel cards |

**Room** (table: [rooms](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#154-170))

| Attribute | Defined in | Used in |
|---|---|---|
| `room_id` INT PK | [database.sql](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/database.sql) line 36 | `/book/{{ room.room_id }}`, `UPDATE rooms SET … WHERE room_id=%s` |
| `room_type` VARCHAR(50) | [database.sql](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/database.sql) line 37 | `request.form["room_type"]` in [add_room()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#378-410), `{{ room.room_type }}` in [rooms.html](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/templates/rooms.html), [my_bookings.html](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/templates/my_bookings.html) |
| `price` DECIMAL(10,2) | [database.sql](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/database.sql) line 38 | `request.form["price"]` in [add_room()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#378-410), `₹{{ room.price }}` in [rooms.html](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/templates/rooms.html) |
| `availability` VARCHAR(20) = 'available' | [database.sql](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/database.sql) line 39 | `{% if room.availability == 'available' %}` in [rooms.html](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/templates/rooms.html), SET in [book()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#174-195) and [cancel_booking()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#225-248) |
| `hotel_id` INT FK | [database.sql](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/database.sql) line 40 | `WHERE hotel_id=%s` in [rooms()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#154-170), `request.form["hotel_id"]` in [add_room()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#378-410) |

**Booking** (table: [bookings](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#199-221))

| Attribute | Defined in | Used in |
|---|---|---|
| `booking_id` INT PK | [database.sql](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/database.sql) line 47 | `/cancel_booking/{{ booking.booking_id }}`, `DELETE WHERE booking_id=%s` |
| `booking_date` DATE | [database.sql](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/database.sql) line 48 | `CURDATE()` set in [book()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#174-195) |
| `check_in` DATE | [database.sql](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/database.sql) line 49 | `CURDATE()` set in [book()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#174-195), `{{ booking.check_in }}` in [my_bookings.html](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/templates/my_bookings.html) |
| `check_out` DATE | [database.sql](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/database.sql) line 50 | `DATE_ADD(CURDATE(), INTERVAL 1 DAY)` in [book()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#174-195), `{{ booking.check_out }}` in [my_bookings.html](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/templates/my_bookings.html) |
| `status` VARCHAR(20) = 'confirmed' | [database.sql](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/database.sql) line 51 | `'confirmed'` set in [book()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#174-195), `{% if booking.status == 'confirmed' %}` in [my_bookings.html](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/templates/my_bookings.html) |
| `user_id` INT FK | [database.sql](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/database.sql) line 52 | `session["user_id"]` passed in [book()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#174-195), `WHERE b.user_id=%s` in [my_bookings()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#199-221) |
| `room_id` INT FK | [database.sql](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/database.sql) line 53 | `room_id` passed in [book()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#174-195), used in [cancel_booking()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#225-248) to free the room |

**Relationships:**
- `User 1 ——< Booking many` : One user makes many bookings. FK `bookings.user_id → users.user_id`
- `Hotel 1 ——< Room many` : One hotel has many rooms. FK `rooms.hotel_id → hotels.hotel_id ON DELETE CASCADE`
- `Room 1 ——< Booking many` : One room can have many bookings (over time). FK `bookings.room_id → rooms.room_id`

---

## 3. Sequence Diagram

![Sequence Diagram](file:///C:/Users/Kartikeya/.gemini/antigravity/brain/355a4c51-01f5-458e-a986-a72f9c9b6c2b/sequence_diagram_1775766975030.png)

### What It Shows
The time-ordered message flow between User, Browser, Flask app, and MySQL during a room booking.

### Every Message Traced to Code

| Step | Message | Code Location |
|---|---|---|
| 1 | `GET /dashboard` | Browser hits `@app.route("/dashboard")` |
| 2 | `HTTP Request /dashboard` | Flask [dashboard()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#119-134) function called |
| 3 | `SELECT * FROM hotels` | `cursor.execute("SELECT * FROM hotels")` in [dashboard()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#119-134) |
| 4 | `hotels[]` returned | `hotels = cursor.fetchall()` |
| 5 | `render_template("dashboard.html", hotels, name)` | `return render_template("dashboard.html", hotels=hotels, name=session.get("user_name"))` |
| 7 | `GET /rooms/{hotel_id}` | `href="/rooms/{{ hotel.hotel_id }}"` in [dashboard.html](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/templates/dashboard.html) |
| 9 | `SELECT * FROM rooms WHERE hotel_id=hotel_id` | `cursor.execute("SELECT * FROM rooms WHERE hotel_id=%s", (hotel_id,))` in [rooms()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#154-170) |
| 11 | `render_template("rooms.html", rooms, hotel_id, hotel_name)` | `return render_template("rooms.html", rooms=rooms, hotel_id=hotel_id, hotel_name=...)` |
| 13 | `GET /book/{room_id}` | `href="/book/{{ room.room_id }}"` in [rooms.html](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/templates/rooms.html) |
| 15 | `Check session["user_id"]` | `if "user_id" not in session: return redirect("/login")` in [book()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#174-195) |
| 16 | `INSERT INTO bookings(...)` | `cursor.execute("""INSERT INTO bookings (booking_date, check_in, check_out, status, user_id, room_id) VALUES (CURDATE(), CURDATE(), DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'confirmed', %s, %s)""", ...)` |
| 17 | `UPDATE rooms SET availability='booked'` | `cursor.execute("UPDATE rooms SET availability='booked' WHERE room_id=%s", (room_id,))` |
| 18 | `OK (commit)` | `db.commit()` in [book()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#174-195) |
| 19 | `flash("Room booked!")` | `flash("Room booked successfully! 🎉", "success")` |
| 20 | `redirect /my_bookings` | `return redirect("/my_bookings")` |

---

## 4. Collaboration Diagram

![Collaboration Diagram](file:///C:/Users/Kartikeya/.gemini/antigravity/brain/355a4c51-01f5-458e-a986-a72f9c9b6c2b/collaboration_diagram_1775766989255.png)

### What It Shows
All objects/components and the messages passed between them (same info as sequence diagram, but shown spatially instead of temporally).

### Every Object and Message Traced to Code

| Object | Code Equivalent |
|---|---|
| `:User` | The browser user (no direct code object) |
| `:Browser / Client` | HTTP client making GET/POST requests |
| `:app.py / Flask` | The Flask application — all `@app.route` functions |
| `:session` | Flask `session` object — `app.config["SESSION_PERMANENT"] = False`, stores `user_id`, `user_name`, `role` |
| `:MySQL DB` | `mysql.connector.connect(host="localhost", user="root", database="hotel_reservation")` in [get_db()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#25-32) |
| `:Template Engine / Jinja2` | `render_template()` calls throughout [app.py](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py) |

| Message # | Message | Code |
|---|---|---|
| 1 | `GET request (URL)` | User navigates to any route like `/dashboard`, `/rooms/1` |
| 5 | `session.get("user_id")` | `if "user_id" not in session` in [dashboard()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#119-134), [book()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#174-195), [my_bookings()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#199-221), [cancel_booking()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#225-248) |
| 6 | `session["role"], session["user_name"]` | `session.get("role") != "admin"` in all admin routes; [inject_user()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#11-14) context processor reads `session.get("user_name")` |
| 7 | `SELECT * FROM users WHERE email=%s` | `cursor.execute("SELECT * FROM users WHERE email=%s", (email,))` in [login()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#75-106) |
| 8 | `INSERT INTO bookings(…)` | Full INSERT in [book()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#174-195) |
| 9 | `UPDATE rooms SET availability='booked'` | In [book()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#174-195) and reversed in [cancel_booking()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#225-248) |
| 10 | `SELECT * FROM hotels/rooms/bookings` | In [dashboard()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#119-134), [rooms()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#154-170), [my_bookings()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#199-221), [admin_bookings()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#285-308), [admin_hotels()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#312-327) |
| 11 | `render_template("dashboard.html", hotels, name)` | `return render_template("dashboard.html", hotels=hotels, name=session.get("user_name"))` |
| 12 | `render_template("rooms.html", rooms, hotel_id, hotel_name)` | `return render_template("rooms.html", rooms=rooms, hotel_id=hotel_id, hotel_name=hotel["hotel_name"])` |

---

## 5. State Diagram

![State Diagram](file:///C:/Users/Kartikeya/.gemini/antigravity/brain/355a4c51-01f5-458e-a986-a72f9c9b6c2b/state_diagram_1775767003568.png)

### What It Shows
The lifecycle of `rooms.availability` and `bookings.status` — the two mutable state fields in the database.

### Every State and Transition Traced to Code

**Room.availability states:**

| State | When Entered | Code |
|---|---|---|
| `available` | Room first created | `'available'` hardcoded in [add_room()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#378-410): `INSERT INTO rooms (…, availability, …) VALUES (…, 'available', …)` |
| `booked` | User books the room | `cursor.execute("UPDATE rooms SET availability='booked' WHERE room_id=%s", (room_id,))` in [book()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#174-195) |
| Back to `available` | Booking cancelled or deleted | `cursor.execute("UPDATE rooms SET availability='available' WHERE room_id=%s", ...)` in [cancel_booking()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#225-248) and [delete_booking()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#414-434) |
| Deleted | Hotel deleted | `DELETE FROM hotels WHERE hotel_id=%s` cascades via `ON DELETE CASCADE` on `rooms.hotel_id` FK |

**Booking.status states:**

| State | When Entered | Code |
|---|---|---|
| `confirmed` | Booking created | `'confirmed'` hardcoded in [book()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#174-195): `INSERT INTO bookings (… status …) VALUES (… 'confirmed' …)` |
| `deleted` | User cancels OR admin deletes | [cancel_booking()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#225-248): `DELETE FROM bookings WHERE booking_id=%s` / [delete_booking()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#414-434): same |

> Note: In this project, `status` doesn't change value — `confirmed` rows are simply deleted rather than updated to `cancelled`. The [my_bookings.html](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/templates/my_bookings.html) has logic for `cancelled` status as a future-proof check.

---

## 6. Component Diagram

![Component Diagram](file:///C:/Users/Kartikeya/.gemini/antigravity/brain/355a4c51-01f5-458e-a986-a72f9c9b6c2b/component_diagram_1775767019181.png)

### What It Shows
The physical/logical architecture — what components exist and how they depend on each other.

### Every Component Traced to Code

| Component | Code Reference |
|---|---|
| **Client Browser** | Receives HTML from Flask, renders [style.css](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/static/style.css) from `static/`, runs the JS in [base.html](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/templates/base.html) (flash auto-dismiss, mobile nav toggle) |
| **Flask Application (app.py)** | The entire [app.py](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py) file. Entry point: `if __name__ == "__main__": app.run(debug=True)` |
| ↳ Route Handler | `@app.route("/")`, `@app.route("/dashboard")`, `@app.route("/rooms/<int:hotel_id>")`, `@app.route("/book/<int:room_id>")`, `@app.route("/my_bookings")`, `@app.route("/cancel_booking/<int:booking_id>")`, `@app.route("/login")`, `@app.route("/register")`, `@app.route("/logout")` |
| ↳ Admin Routes | `@app.route("/admin_dashboard")`, `@app.route("/admin_bookings")`, `@app.route("/admin_hotels")`, `@app.route("/add_hotel")`, `@app.route("/add_room")`, `@app.route("/delete_hotel/<int:hotel_id>")`, `@app.route("/delete_booking/<int:booking_id>")` |
| ↳ Context Processor | `@app.context_processor def inject_user()` — injects `user=session.get("user_name")` into every template so `{{ user }}` works in [base.html](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/templates/base.html) navbar |
| ↳ After Request Hook | `@app.after_request def add_no_cache_headers()` — adds `Cache-Control: no-cache, no-store, must-revalidate` to prevent back-button leaking logged-in pages |
| **Jinja2 Template Engine** | `render_template()` built into Flask. Processes [base.html](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/templates/base.html), `{% extends "base.html" %}`, `{% block content %}`, `{% for %}`, `{% if %}`, `{{ variable }}` in all templates |
| **MySQL Database** | `mysql.connector.connect(host="localhost", user="root", password="…", database="hotel_reservation")` in [get_db()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#25-32). Contains tables: `users`, [hotels](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#138-150), [rooms](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#154-170), [bookings](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#199-221) |
| **Flask-Bcrypt** | `from flask_bcrypt import Bcrypt; bcrypt = Bcrypt(app)`. Used: `bcrypt.generate_password_hash(password)` in [register()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#43-71), `bcrypt.check_password_hash(user["password"], password)` in [login()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#75-106) |
| **Session Store** | `app.secret_key = "supersecretkey"` enables Flask's cookie-based session. Stores `user_id`, `user_name`, `role`. Read by [inject_user()](file:///c:/Users/Kartikeya/Projects/Hotel%20reservation%28software%20engine.%29/app.py#11-14) and every protected route |

---

## Regeneration Prompts

> Copy-paste these into Gemini image generation to recreate any diagram.

````carousel
**Activity Diagram Prompt:**
```
Professional UML Activity Diagram for a Hotel Reservation System on a pure white background, clean black lines, standard UML notation. Title: "Activity Diagram — Hotel Reservation System". Two swimlanes: "User" and "System". Flow: Start → Visit Homepage → Decision "Logged in?" → No path: Click Login → Validate Credentials → Decision "Valid?" → No: Show Error → back to Login; Yes: Create Session (user_id, user_name, role) → Decision "Role==admin?" → Yes: Redirect /admin_dashboard; No: Redirect /dashboard → Browse Hotels (SELECT * FROM hotels) → Click View Rooms → Load Rooms (SELECT * FROM rooms WHERE hotel_id) → Decision "Room available?" → No: Show Not Available; Yes: Click Book Now → INSERT INTO bookings + UPDATE rooms SET availability='booked' → Flash "Room booked!" → Redirect /my_bookings → Cancel Booking → DELETE FROM bookings + UPDATE rooms SET availability='available' → End. Blue swimlane headers, standard UML shapes.
```
<!-- slide -->
**Class Diagram Prompt:**
```
Professional UML Class Diagram on white background. Title: "Class Diagram — Hotel Reservation System". 4 classes: (1) User: user_id INT PK, name VARCHAR(100), email VARCHAR(100), password VARCHAR(255), role VARCHAR(20)='customer', created_at TIMESTAMP; methods: register(), login(), logout(). (2) Hotel: hotel_id INT PK, hotel_name VARCHAR(150), location VARCHAR(200), description TEXT, created_at TIMESTAMP; methods: add_hotel(), delete_hotel(), view_hotels(). (3) Room: room_id INT PK, room_type VARCHAR(50), price DECIMAL(10,2), availability VARCHAR(20)='available', hotel_id INT FK; methods: add_room(), book_room(), cancel_booking(). (4) Booking: booking_id INT PK, booking_date DATE, check_in DATE, check_out DATE, status VARCHAR(20)='confirmed', user_id INT FK, room_id INT FK, created_at TIMESTAMP; methods: create_booking(), delete_booking(). Relationships: User 1—<* Booking (makes), Hotel 1—<* Room (has), Room 1—<* Booking (linked to). Blue class headers, crow's foot notation.
```
<!-- slide -->
**Sequence Diagram Prompt:**
```
Professional UML Sequence Diagram. Title: "Sequence Diagram — Book a Hotel Room". Lifelines: :User (stick figure), :Browser, :Flask App (app.py), :MySQL Database. Messages (numbered): 1. User→Browser: GET /dashboard, 2. Browser→Flask: HTTP Request, 3. Flask→MySQL: SELECT * FROM hotels, 4. MySQL→Flask: hotels[], 5. Flask→Browser: render_template("dashboard.html", hotels, name), 6. Browser→User: Show hotels, 7. User→Browser: GET /rooms/hotel_id, 8. Browser→Flask: HTTP Request, 9. Flask→MySQL: SELECT * FROM rooms WHERE hotel_id=hotel_id, 10. MySQL→Flask: rooms[], 11. Flask→Browser: render_template("rooms.html", rooms, hotel_id, hotel_name), 12. Browser→User: Show rooms with Book Now, 13. User→Browser: GET /book/room_id, 14. Browser→Flask: HTTP Request, 15. Flask self: Check session["user_id"], 16. Flask→MySQL: INSERT INTO bookings (booking_date,check_in,check_out,status,user_id,room_id), 17. Flask→MySQL: UPDATE rooms SET availability='booked', 18. MySQL→Flask: OK commit, 19. Flask self: flash("Room booked!"), 20. Flask→Browser: redirect /my_bookings, 21. Browser→User: Show My Bookings. White background, activation boxes, blue system headers.
```
<!-- slide -->
**Collaboration Diagram Prompt:**
```
Professional UML Collaboration Diagram (Communication Diagram). Title: "Collaboration Diagram — Hotel Reservation System". Objects as rectangles: :User, :Browser/Client, :app.py/Flask (center), :session (stores user_id,user_name,role), :MySQL DB (tables:users,hotels,rooms,bookings), :Template Engine/Jinja2. Numbered messages on connecting lines: User↔Browser: 1:GET request, 2:HTML response. Browser↔Flask: 3:HTTP request, 4:HTTP response. Flask↔session: 5:session.get("user_id"), 6:session["role"],session["user_name"]. Flask↔MySQL: 7:SELECT * FROM users WHERE email=%s, 8:INSERT INTO bookings, 9:UPDATE rooms SET availability='booked', 10:SELECT * FROM hotels/rooms/bookings. Flask↔Jinja2: 11:render_template("dashboard.html",hotels,name), 12:render_template("rooms.html",rooms,hotel_id,hotel_name). Blue rectangles, black arrows, white background.
```
<!-- slide -->
**State Diagram Prompt:**
```
Professional UML State Diagram. Title: "State Diagram — Room & Booking Lifecycle". Two state machines side by side. LEFT — Room.availability: Initial state●→available [add_room() INSERT availability='available']→booked [book() UPDATE rooms SET availability='booked']→available [cancel_booking()/delete_booking() UPDATE rooms SET availability='available']; booked→⊙ [delete_hotel() CASCADE]. RIGHT — Booking.status: Initial state●→confirmed [book() INSERT status='confirmed']→deleted [cancel_booking() DELETE FROM bookings OR delete_booking() DELETE FROM bookings]→⊙. Blue state boxes, black arrows, field names and SQL as transition labels, white background.
```
<!-- slide -->
**Component Diagram Prompt:**
```
Professional UML Component Diagram. Title: "Component Diagram — Hotel Reservation System". Components with UML notation: (1)<<component>>Client Browser [templates: index.html,login.html,register.html,dashboard.html,rooms.html,my_bookings.html,admin_dashboard.html etc, static/style.css]. (2)<<component>>Flask Application(app.py) [sub-modules: Route Handler(home,login,register,logout,dashboard,rooms,book,my_bookings,cancel_booking), Admin Routes(admin_dashboard,admin_bookings,admin_hotels,add_hotel,add_room,delete_hotel,delete_booking), Context Processor inject_user()→user variable, After Request Hook add_no_cache_headers()→Cache-Control]. (3)<<component>>Jinja2 Template Engine [base.html, render_template()]. (4)<<component>>MySQL Database [tables:users,hotels,rooms,bookings, get_db() mysql.connector.connect()]. (5)<<component>>Flask-Bcrypt [generate_password_hash(),check_password_hash()]. (6)<<component>>Session Store [user_id,user_name,role, secret_key]. Connections: Browser→Flask(HTTP), Flask→Jinja2(render_template), Flask→MySQL(SQL), Flask→Bcrypt(passwords), Flask↔Session. Blue components, lollipop interfaces, white background.
```
````
