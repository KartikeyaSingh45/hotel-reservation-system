-- ===============================================
-- Hotel Reservation System Database (Final Version)
-- ===============================================

CREATE DATABASE IF NOT EXISTS hotel_reservation;
USE hotel_reservation;

-- ===============================================
-- USERS TABLE
-- ===============================================
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'customer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================================
-- HOTELS TABLE
-- ===============================================
CREATE TABLE hotels (
    hotel_id INT AUTO_INCREMENT PRIMARY KEY,
    hotel_name VARCHAR(150) NOT NULL,
    location VARCHAR(200) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================================
-- ROOMS TABLE
-- ===============================================
CREATE TABLE rooms (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    room_type VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    availability VARCHAR(20) DEFAULT 'available',
    hotel_id INT NOT NULL,
    FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id) ON DELETE CASCADE
);

-- ===============================================
-- BOOKINGS TABLE
-- ===============================================
CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_date DATE NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'confirmed',
    user_id INT NOT NULL,
    room_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES rooms(room_id) ON DELETE CASCADE
);

-- ===============================================
-- SAMPLE DATA (FOR TESTING)
-- ===============================================

-- Hotels
INSERT INTO hotels (hotel_name, location, description) VALUES
('The Grand Palace', 'Shimla', 'Luxury hotel with mountain views'),
('Hotel Sunrise', 'Manali', 'Cozy hotel near the Beas river');

-- Rooms
INSERT INTO rooms (room_type, price, availability, hotel_id) VALUES
('Single', 1500.00, 'available', 1),
('Double', 2500.00, 'available', 1),
('Suite', 5000.00, 'available', 1),
('Single', 1200.00, 'available', 2),
('Double', 2000.00, 'available', 2);

-- OPTIONAL: ADMIN USER (UNCOMMENT IF YOU ADD REAL HASH)
-- Password: admin123 (must be bcrypt hash from Flask)
-- INSERT INTO users (name, email, password, role) VALUES
-- ('Admin', 'admin@hotel.com', 'PUT_BCRYPT_HASH_HERE', 'admin');