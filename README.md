Login System with User Authentication

📌 Project Overview

This project is a Login System built with Python Flask that includes user authentication features like registration, login, password recovery, and user data management. It securely stores user details using MySQL.

🚀 Features

✅ User Registration – Secure sign-up with input validation✅ User Login – Authenticate users with email & password✅ Forgot Password Recovery – Allows users to reset passwords securely✅ User Data Management – Store and manage user details in a MySQL database✅ Session Management – Ensures secure user authentication & access

🛠️ Tech Stack

Backend: Python Flask

Frontend: HTML, CSS, Bootstrap

Database: MySQL

Security: Password hashing (bcrypt)

📂 Project Structure

Login-System/
│── app.py          # Main Flask application
│── config.py       # Configuration settings
│── templates/      # HTML templates (Login, Register, Dashboard, etc.)
│── static/         # CSS & JS files
│── database.sql    # MySQL database schema
│── requirements.txt # Dependencies

🛠️ Setup & Installation

1️⃣ Clone the repository

git clone https://github.com/your-repo/login-system.git
cd login-system

2️⃣ Install dependencies

pip install -r requirements.txt

3️⃣ Set up MySQL Database

Create a new MySQL database

Import the database.sql file to set up tables

Update config.py with your database credentials

4️⃣ Run the Application

python app.py

Access the app in your browser at: http://127.0.0.1:5000

🔒 Security Measures

Password Hashing: Uses bcrypt for secure password storage

Session Management: Ensures authenticated user access

Input Validation: Prevents SQL Injection & XSS attacks

📌 Future Enhancements

🔹 Implement email verification during registration🔹 Add two-factor authentication (2FA) for extra security🔹 Improve UI/UX for better user experience

🤝 Contributors

🚀 Developed by N Shalem Raju💡 

📢 Feel free to contribute or share your feedback!

💬 Let’s build secure & scalable authentication systems together!
