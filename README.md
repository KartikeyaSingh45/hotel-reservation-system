# 🏨 Hotel Reservation System

A full-stack web application that allows users to browse hotels, view available rooms, and make bookings. The system also includes an admin panel to manage hotels, rooms, and bookings.

---

## 🚀 Features

### 👤 User Features
- User Registration & Login (with secure authentication)
- Browse hotels and view room details
- Book available rooms
- Cancel bookings
- View personal booking history
- Session-based login system

---

### 🔐 Admin Features
- Admin login system
- Add new hotels
- Add rooms to hotels
- View all bookings (with user details)
- Delete bookings
- Delete hotels

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python (Flask)
- **Database:** MySQL
- **Authentication:** Flask Sessions + Bcrypt

---

## 📂 Project Structure

hotel-reservation-system/
│
├── app.py
├── database.sql
├── templates/
├── static/
├── README.md

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/hotel-reservation-system.git
cd hotel-reservation-system

---

### 2️⃣ Install Dependencies

pip install flask flask-bcrypt mysql-connector-python

---

### 3️⃣ Setup Database

Open MySQL and run:

- source database.sql;

This will:

-Create database
-Create tables
-Insert sample data

---

### 4️⃣ Configure Database in app.py

Open app.py and update:

- host="localhost"
- user="root"
- password="your_mysql_password"
- database="hotel_reservation"

---

### 5️⃣ Run the Application

- python app.py

---

### 6️⃣ Open in Browser

- http://127.0.0.1:5000

---

### Admin Setup

After registering a user, run this query in MySQL:

- UPDATE users SET role='admin' WHERE email='your_email@gmail.com';

Then login via:

- /admin_login

---

### 🔁 Workflow

- User Flow

Landing Page → View Hotels → View Rooms → Book → My Bookings → Cancel

- Admin Flow

Admin Login → Dashboard → Add Hotel/Room → Manage Bookings → Delete

---

### Screenshots

---

### ⚠️ Important Notes

- Do not share your MySQL password
- Update DB credentials before running
- Ensure MySQL server is running

---

### 🚀 Future Improvements

- Date selection for booking
- Payment gateway integration
- Email notifications
- Cloud deployment (AWS / Supabase)
- Modern UI design

---

### 👨‍💻 Author

Kartikeya Singh
