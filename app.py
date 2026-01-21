from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

UNIVERSITY_EMAIL = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"   # Use Gmail App Password

COURSE_FEES = {
    "MBA": "₹1,20,000",
    "B.Tech": "₹1,50,000",
    "MCA": "₹1,00,000"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register/<course>")
def register(course):
    return render_template("register.html", course=course, fee=COURSE_FEES[course])

@app.route("/payment", methods=["POST"])
def payment():
    name = request.form["name"]
    email = request.form["email"]
    course = request.form["course"]
    fee = COURSE_FEES[course]

    return render_template("payment.html", name=name, email=email, course=course, fee=fee)

@app.route("/success", methods=["POST"])
def success():
    name = request.form["name"]
    email = request.form["email"]
    course = request.form["course"]
    fee = request.form["fee"]
    payment_method = request.form["payment"]

    send_email(name, email, course, fee, payment_method)
    return render_template("success.html")

def send_email(name, email, course, fee, payment_method):
    msg = EmailMessage()
    msg["Subject"] = "Invertis University | Course Enrollment Confirmation"
    msg["From"] = UNIVERSITY_EMAIL
    msg["To"] = email

    msg.set_content(f"""
Dear {name},

Congratulations 🎉

Your admission is confirmed at Invertis University.

Course: {course}
Amount Paid: {fee}
Payment Method: {payment_method}

Invoice ID: INV-2026-UNI

Thank you for choosing Invertis University.

Regards,
Invertis University Admission Team
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(UNIVERSITY_EMAIL, EMAIL_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
