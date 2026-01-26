from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
from datetime import datetime
import os

# PDF
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- APP CONFIG ----------------
app = Flask(__name__)
app.secret_key = "secret123"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------------- LOAD ML MODEL ----------------
model = joblib.load("blood_donation_model.pkl")

blood_group_map = {
    'A+': 0, 'A-': 1, 'B+': 2, 'B-': 3,
    'AB+': 4, 'AB-': 5, 'O+': 6, 'O-': 7
}

gender_map = {'Male': 0, 'Female': 1}

# ---------------- USER MODEL ----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            session["user"] = user.username
            return redirect(url_for("home"))
        flash("Invalid username or password", "danger")
    return render_template("login.html")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if User.query.filter_by(username=request.form["username"]).first():
            flash("User already exists", "warning")
            return redirect(url_for("register"))

        user = User(
            username=request.form["username"],
            password=generate_password_hash(request.form["password"])
        )
        db.session.add(user)
        db.session.commit()

        flash("Registration successful!", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# ---------------- FORGOT PASSWORD ----------------
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        if password != confirm:
            flash("Passwords do not match", "danger")
            return redirect(url_for("forgot_password"))

        user = User.query.filter_by(username=username).first()
        if not user:
            flash("User not found", "danger")
            return redirect(url_for("forgot_password"))

        user.password = generate_password_hash(password)
        db.session.commit()

        flash("Password reset successful!", "success")
        return redirect(url_for("login"))

    return render_template("forgot_password.html")

# ---------------- HOME ----------------
@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("home.html")

# ---------------- PREDICTION ----------------
@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        age = int(request.form["age"])
        weight = int(request.form["weight"])
        blood_group = request.form["blood_group"]
        months = int(request.form["months_since_last_donation"])
        total = int(request.form["total_donations"])
        gender = request.form["gender"]

        if age < 18 or weight < 45:
            eligibility = "Not Eligible"
            result = "❌ Not Eligible"
        else:
            data = [[age, weight, blood_group_map[blood_group], months, total, gender_map[gender]]]
            prediction = model.predict(data)[0]
            eligibility = "Eligible" if prediction == 1 else "Not Eligible"
            result = "🎉 Eligible Donor" if prediction == 1 else "⚠️ Not Eligible Right Now"

        session["report"] = {
            "username": session["user"],
            "age": age,
            "weight": weight,
            "blood_group": blood_group,
            "gender": gender,
            "months": months,
            "total": total,
            "eligibility": eligibility,
            "date": datetime.now().strftime("%d %b %Y, %I:%M %p")
        }

        flash(result, "success" if eligibility == "Eligible" else "danger")
        return redirect(url_for("report"))

    return render_template("prediction.html")

# ---------------- REPORT ----------------
@app.route("/report")
def report():
    if "report" not in session:
        return redirect(url_for("prediction"))
    return render_template("report.html", report=session["report"])

# ---------------- DOWNLOAD PDF ----------------
@app.route("/download-report")
def download_report():
    if "report" not in session:
        return redirect(url_for("prediction"))

    report = session["report"]

    os.makedirs("reports", exist_ok=True)
    filename = f"reports/{report['username']}_blood_report.pdf"

    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Blood Donation Eligibility Report", styles["Title"]))
    story.append(Spacer(1, 20))

    for key, value in report.items():
        story.append(Paragraph(f"<b>{key.capitalize()}:</b> {value}", styles["Normal"]))
        story.append(Spacer(1, 10))

    doc.build(story)

    return send_file(filename, as_attachment=True)

# ---------------- OTHER PAGES ----------------
@app.route("/about")
def about():
    return render_template("about_us.html")

@app.route("/tips")
def tips():
    return render_template("tips.html")

@app.route("/contact")
def contact():
    return render_template("contact_us.html")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
