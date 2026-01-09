from flask import Flask, render_template, redirect, url_for, request, flash, send_file
from flask_mail import Mail, Message
from datetime import datetime
from io import BytesIO
from xhtml2pdf import pisa
from models import db, StudentEnrolment
import os
from flask import send_from_directory

from app import app, db
with app.app_context():
    db.create_all()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'your_database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False





app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'info@goldwingsaviation.com.au'          # Your email
app.config['MAIL_PASSWORD'] = 'Almasg@2025'             # Your password or app password
app.config['MAIL_DEFAULT_SENDER'] = 'info@goldwingsaviation.com.au'    # default sender

mail = Mail(app)


mail = Mail(app)

# Init DB
db.init_app(app)

def generate_enrolment_pdf(enrolment):
    html = render_template("enrolment_pdf.html", enrolment=enrolment)
    pdf = BytesIO()
    pisa.CreatePDF(html, dest=pdf)
    pdf.seek(0)
    return pdf


@app.route('/robots.txt')
def robots_txt():
    return send_from_directory('static', 'robots.txt')

@app.route('/sitemap.xml')
def sitemap_xml():
    return send_from_directory('static', 'sitemap.xml')

@app.route('/')
def home():
    return render_template("home.html", page="Home")

@app.route('/about')
def about():
    return render_template("about.html", page="About")

@app.route('/services')
def services():
    return render_template("service.html", page="Services")
@app.route('/pilot-training-cost-melbourne')
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

@app.route('/recreational-pilot-licence-melbourne')
def rpl():
    return render_template("rpl.html", page="RPL")

@app.route('/tif')
def cpl():
    return render_template("tif.html", page="TIF")

@app.route('/private-pilot-licence-melbourne')
def ppl():
    return render_template("ppl.html", page="PPL")

@app.route("/ppl")
def old_ppl():
    return redirect("/private-pilot-licence-melbourne", code=301)

@app.route("/rpl")
def old_rpl():
    return redirect("/recreational-pilot-licence-melbourne", code=301)

@app.route("/pricing")
def old_pricing():
    return redirect("/pilot-training-cost-melbourne", code=301)

@app.route('/end')
def end():
    return render_template('end.html')

@app.route("/blog/pilot-training-cost-melbourne")
def pilot_training_cost():
    return render_template("training-cost.html")

@app.route("/blog/Weather-Conditions-for-Flying-in-Melbourne")
def weather():
    return render_template("weather.html")

@app.route('/mission')
def mission():
    return render_template('mission.html', page="Our Mission")
@app.route('/blog')
def blog():
    return render_template('blog.html', page="Our Blog")
@app.route('/blog/rpl-vs-ppl')
def rpl_vs_ppl():
    return render_template('rpl-vs-ppl-melbourne.html')
@app.route('/blog/flight-school-moorabbin')
def flight_school_moorabbin():
    return render_template('flight-school-moorabbin.html')
@app.route("/blog/learn-to-fly-melbourne-vs-australia")
def learn_to_fly_melbourne_vs_australia():
    return render_template("learning-to-fly-melbourne-vs-australia.html")
@app.route("/pilot-training-faq-melbourne")
def pilot_training_faq_melbourne():
    return render_template("pilot-training-faq-melbourne.html")

@app.route('/values')
def values():
    return render_template('values.html', page="Our Values")

@app.route('/student-enrolment', methods=['GET', 'POST'])
def student_enrolment():
    if request.method == 'POST':

        goals = request.form.getlist('flying_goals')

        enrolment = StudentEnrolment(
            date=datetime.strptime(request.form['date'], '%Y-%m-%d') if request.form.get('date') else None,
            arn=request.form.get('arn'),

            surname=request.form['surname'],
            first_names=request.form['first_names'],
            date_of_birth=datetime.strptime(request.form['dob'], '%Y-%m-%d'),
            gender=request.form.get('gender'),

            street_address=request.form['street_address'],
            suburb=request.form['suburb'],
            postcode=request.form['postcode'],
            state=request.form['state'],
            country=request.form['country'],

            mobile=request.form['mobile'],
            email=request.form['email'],

            emergency_name=request.form['emergency_name'],
            emergency_relationship=request.form['emergency_relationship'],
            emergency_mobile=request.form['emergency_mobile'],

            flying_hours=request.form.get('flying_hours'),
            license_type=request.form.get('license_type'),
            flying_goals=", ".join(goals)
        )

        # 1️⃣ Save to database
        db.session.add(enrolment)
        db.session.commit()

        # 2️⃣ Generate PDF from HTML template
        html = render_template('enrolment_pdf.html', enrolment=enrolment)
        pdf_buffer = BytesIO()
        pisa.CreatePDF(html, dest=pdf_buffer)
        pdf_buffer.seek(0)

        # 3️⃣ Send email with PDF attachment
        msg = Message(
            subject=f"{enrolment.first_names} {enrolment.surname} submitted the enrolment form",
            sender=app.config['MAIL_USERNAME'],
            recipients=['info@goldwingsaviation.com.au']
        )

        msg.body = (
            "A new student enrolment form has been submitted.\n\n"
            "Please find the completed enrolment form attached as a PDF."
        )

        msg.attach(
            filename=f"Student_Enrolment_{enrolment.first_names}_{enrolment.surname}.pdf",
            content_type="application/pdf",
            data=pdf_buffer.read()
        )

        mail.send(msg)

        # 4️⃣ Success + redirect
        flash("Your enrolment has been submitted successfully.", "success")
        return redirect(url_for('end'))

    return render_template('student_enrolment.html', page="Student Enrolment")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
