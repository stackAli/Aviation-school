from flask import Flask, render_template, redirect, url_for, request, flash, send_file
from flask_mail import Mail, Message
from models import db, UserProfile, EducationDetail, LanguageSkill, User
from datetime import datetime
from io import BytesIO
from xhtml2pdf import pisa
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secure email configuration
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# Load values from environment variables
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")       # email
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")       # app password
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USERNAME") # default sender

mail = Mail(app)


mail = Mail(app)

# Init DB
db.init_app(app)

@app.route('/')
def home():
    return render_template("home.html", page="Home")

@app.route('/about')
def about():
    return render_template("about.html", page="About")

@app.route('/services')
def services():
    return render_template("service.html", page="Services")
@app.route('/pricing')
def pricing():
    return render_template('pricing.html', page="Pricing")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        msg = Message(
            subject="New Contact Query",
            sender=app.config['MAIL_USERNAME'],  # ✅ Explicitly set sender here
            recipients=['info@goldwingsaviation.com.au']
        )
        msg.body = f"You have received a new contact message:\n\nName: {name}\nEmail: {email}\n\nMessage:\n{message}"
        
        mail.send(msg)

        flash("Your message has been sent successfully!", "success")
        return redirect(url_for('end'))

    return render_template("contact.html", page="Contact")

@app.route('/rpl')
def rpl():
    return render_template("rpl.html", page="RPL")

@app.route('/tif')
def cpl():
    return render_template("tif.html", page="TIF")

@app.route('/ppl')
def ppl():
    return render_template("ppl.html", page="PPL")


@app.route('/end')
def end():
    return render_template('end.html')


@app.route('/mission')
def mission():
    return render_template('mission.html', page="Our Mission")

@app.route('/values')
def values():
    return render_template('values.html', page="Our Values")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
