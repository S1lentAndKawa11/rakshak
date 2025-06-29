# 🛡️ Rakshak – Emergency Assistance Platform

Rakshak is a community-driven web application built to facilitate faster emergency response, donor-volunteer collaboration, and real-time story sharing. It empowers users, volunteers, and admins to act swiftly in crisis situations with features like emergency SMS alerts, registration portals, and more.

---

## 🌐 Features

- 🧾 **User Registration & Login** – Register as user or admin with secure hashed passwords.
- 🔐 **Admin Panel** – Exclusive admin dashboard for overseeing community activities.
- 📢 **Forum** – Share helping stories to inspire others and build a volunteer portfolio.
- 🤝 **Volunteer Registration** – Sign up as a volunteer and list your availability.
- 🎁 **Donor Registration** – Become a verified donor by filling out your details.
- 🚨 **Emergency SMS Feature** – One-click SOS button to send SMS alerts to saved contacts.
- 🎨 **Responsive UI** – Clean, minimalistic UI with Bootstrap 5 styling.
- ✅ **Session-based Authentication** – Secured user sessions for accessing dashboards.
- 🛠️ **MySQL Integration Ready** – Database setup for storing persistent data.

---

## 📸 Screenshots

> (Add screenshots here showing homepage, forum, admin panel, SOS popup, etc.)

---

## 🚀 Tech Stack

| Category         | Tools Used                      |
|------------------|----------------------------------|
| Backend          | Flask, Python, Flask-WTF         |
| Frontend         | HTML5, Bootstrap 5, Jinja2       |
| Database         | MySQL                            |
| Authentication   | Flask-Bcrypt, Flask Session      |
| SMS API          | Textbelt API (Free for testing)  |

---

## 🏁 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/rakshak.git
cd rakshak
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
pip install -r requirements.txt
python run.py
SECRET_KEY=your_flask_secret_key
TEXTBELT_KEY=textbelt
```
