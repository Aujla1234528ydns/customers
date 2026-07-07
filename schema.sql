CREATE DATABASE IF NOT EXISTS customers;

USE customers;

DROP TABLE IF EXISTS admins;
DROP TABLE IF EXISTS customers;

CREATE TABLE admins(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO admins(username,password)
VALUES
('admin','aniket_admin');

CREATE TABLE customers(

    id INT AUTO_INCREMENT PRIMARY KEY,

    full_name VARCHAR(100) NOT NULL,

    father_name VARCHAR(100),

    mother_name VARCHAR(100),

    dob DATE,

    gender VARCHAR(20),

    occupation VARCHAR(100),

    mobile VARCHAR(15),

    alternate_mobile VARCHAR(15),

    email VARCHAR(100),

    address TEXT,

    city VARCHAR(100),

    state VARCHAR(100),

    pincode VARCHAR(10),

    remarks TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);