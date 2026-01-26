from flask import Flask, render_template, request, redirect, session, send_file
import sqlite3
from fpdf import FPDF
from datetime import datetime

app = Flask(__name__)
app.secret_key = "movie_secret_key"

# ---------------- MOVIES ----------------
MOVIES = {
    "Avengers": {"price": 200, "screen": "Screen 1", "times": ["10:00 AM", "2:00 PM", "6:00 PM"]},
    "Batman": {"price": 180, "screen": "Screen 2", "times": ["11:00 AM", "3:00 PM", "7:00 PM"]},
    "Jawan": {"price": 220, "screen": "Screen 3", "times": ["9:30 AM", "1:30 PM", "5:30 PM"]}
}

# ---------------- SEATS ----------------
ALL_SEATS = [
    "A1","A2","A3","A4","A5",
    "B1","B2","B3","B4","B5",
    "C1","C2","C3","C4","C5",
    "D1","D2","D3","D4","D5",
    "E1","E2","E3","E4"
]

# ---------------- DATABASE ----------------
def db():
    return sqlite3.connect("users.db")

def init_db():
    con = db()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS seats (
            movie TEXT,
            seat_no TEXT,
            user TEXT
        )
    """)
    con.commit()
    con.close()

init_db()

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        con = db()
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
        user = cur.fetchone()
        con.close()
        if user:
            session["user"] = u
            return redirect("/movies")
    return render_template("login.html")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        con = db()
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO users VALUES (?,?)", (u, p))
            con.commit()
        except sqlite3.IntegrityError:
            con.close()
            return "Username already exists!"
        con.close()
        return redirect("/")
    return render_template("register.html")

# ---------------- MOVIES ----------------
@app.route("/movies")
def movies():
    if "user" not in session:
        return redirect("/")
    return render_template("movies.html", movies=MOVIES)

# ---------------- SEATS ----------------
@app.route("/seats/<movie>", methods=["GET", "POST"])
def seats(movie):
    if "user" not in session:
        return redirect("/")

    con = db()
    cur = con.cursor()
    cur.execute("SELECT seat_no FROM seats WHERE movie=?", (movie,))
    booked_seats = [row[0] for row in cur.fetchall()]
    available_seats = [s for s in ALL_SEATS if s not in booked_seats]

    if request.method == "POST":
        selected_seats = request.form.getlist("seat")
        show_time = request.form.get("show_time")
        payment_type = request.form.get("payment")

        for seat in selected_seats:
            if seat in booked_seats:
                return "Seat already booked!"

        for seat in selected_seats:
            cur.execute("INSERT INTO seats VALUES (?,?,?)",
                        (movie, seat, session["user"]))

        con.commit()
        con.close()

        amount = len(selected_seats) * MOVIES[movie]["price"]
        booking_time = datetime.now().strftime("%d %b %Y | %I:%M %p")
        screen_no = MOVIES[movie]["screen"]

        session["ticket"] = (
            movie,
            selected_seats,
            amount,
            booking_time,
            show_time,
            screen_no,
            payment_type,
            "PAID"
        )

        return redirect("/success")

    con.close()
    return render_template(
        "seats.html",
        movie=movie,
        available_seats=available_seats,
        booked_seats=booked_seats,
        show_times=MOVIES[movie]["times"]
    )

# ---------------- SUCCESS + PDF ----------------
@app.route("/success")
def success():
    if "ticket" not in session:
        return redirect("/movies")

    (movie, seats, amount, booking_time,
     show_time, screen_no, payment_type, status) = session["ticket"]

    user = session["user"]

    pdf = FPDF()
    pdf.add_page()

    # Background
    pdf.set_fill_color(245, 245, 245)
    pdf.rect(0, 0, 210, 297, "F")

    # Header
    pdf.set_fill_color(30, 30, 30)
    pdf.rect(15, 20, 180, 25, "F")
    pdf.set_font("Arial", "B", 22)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(15, 26)
    pdf.cell(180, 10, "MOVIE E-TICKET", align="C")

    # Movie name
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 18)
    pdf.set_xy(20, 55)
    pdf.cell(0, 10, movie)
    pdf.line(20, 68, 190, 68)

    # Ticket details
    pdf.set_font("Arial", "", 14)
    y = 75
    pdf.set_xy(25, y); pdf.cell(0, 10, f"Customer : {user}")
    pdf.set_xy(25, y+10); pdf.cell(0, 10, f"Screen : {screen_no}")
    pdf.set_xy(25, y+20); pdf.cell(0, 10, f"Show Time : {show_time}")
    pdf.set_xy(25, y+30); pdf.cell(0, 10, f"Payment : {payment_type}")
    pdf.set_xy(25, y+40); pdf.cell(0, 10, f"Status : {status}")
    pdf.set_xy(25, y+50); pdf.cell(0, 10, f"Amount : Rs. {amount}")
    pdf.set_xy(25, y+60); pdf.cell(0, 10, f"Booked : {booking_time}")

    # Seats Box on the right
    pdf.set_fill_color(220, 20, 60)
    pdf.rect(120, 75, 60, 40, "F")  # Red rectangle
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(120, 82)
    pdf.multi_cell(60, 10, "SEAT\n" + ", ".join(seats), align="C")

    # Footer
    pdf.set_text_color(120, 120, 120)
    pdf.set_font("Arial", "I", 11)
    pdf.set_xy(15, 160)
    pdf.cell(180, 8, "Enjoy your movie | Movie Ticket Booking System", align="C")

    pdf.output("ticket.pdf")

    return render_template(
        "success.html",
        movie=movie,
        seats=seats,
        amount=amount,
        show_time=show_time,
        screen_no=screen_no,
        booking_time=booking_time,
        payment_type=payment_type,
        status=status
    )

# ---------------- DOWNLOAD ----------------
@app.route("/download")
def download():
    return send_file("ticket.pdf", as_attachment=True)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
