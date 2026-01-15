from flask import Flask, render_template, request, redirect, url_for, session
from services import db, get_status, generate_timetable
from datetime import datetime
import random
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "techsprint_secret")

def get_camera_density():
    return random.randint(10, 95)

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    user_type = request.form.get("user_type")

    if user_type == "student":
        session["user_type"] = "student"
        session["logged_in"] = True
        return redirect(url_for("dashboard"))

    if user_type == "faculty":
        reg_id = request.form.get("reg_id")
        access_code = request.form.get("access_code")
        doc = db.collection("faculties").document(reg_id).get()
        
        if doc.exists and doc.to_dict().get("access_code") == access_code:
            session["user_type"] = "faculty"
            session["faculty"] = reg_id
            session["logged_in"] = True
            return redirect(url_for("admin"))
        
        return render_template("login.html", error="Invalid credentials")

    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("home"))

    demo_time = request.args.get("time")
    OPEN_HOUR = 9
    CLOSE_HOUR = 17

    if not demo_time:
        return render_template("dashboard.html", rooms=[], demo_time=None,
                             message="Please choose a time to view room availability.")

    hour, minute = map(int, demo_time.split(":"))

    if hour < OPEN_HOUR or hour >= CLOSE_HOUR:
        return render_template("dashboard.html", rooms=[], demo_time=demo_time,
                             message="University is closed. Opens at 9:00 AM.")

    room_docs = list(db.collection("rooms").stream())
    room_ids = [r.id for r in room_docs]

    if "timetable" not in session:
        session["timetable"] = generate_timetable(room_ids)

    timetable = session["timetable"]
    overrides = [o.to_dict() for o in db.collection("room_overrides").stream()]
    rooms = []

    for room in room_docs:
        data = room.to_dict()
        status, next_available = get_status(room.id, timetable, demo_time, overrides)
        
        room_payload = {
            "id": room.id,
            "type": data.get("type"),
            "capacity": data.get("capacity"),
            "status": status,
            "next_available": next_available
        }

        if status == "Available":
            room_payload["density"] = get_camera_density()

        rooms.append(room_payload)

    return render_template("dashboard.html", rooms=rooms, demo_time=demo_time, message=None)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if "faculty" not in session:
        return redirect(url_for("home"))

    demo_time = request.args.get("time", datetime.now().strftime("%H:%M"))
    room_docs = list(db.collection("rooms").stream())
    room_ids = [r.id for r in room_docs]

    if "timetable" not in session:
        session["timetable"] = generate_timetable(room_ids)

    timetable = session["timetable"]
    overrides = [o.to_dict() for o in db.collection("room_overrides").stream()]

    if request.method == "POST":
        db.collection("room_overrides").add({
            "room_id": request.form["room_id"],
            "type": request.form["action"],
            "start_time": demo_time,
            "end_time": request.form["till_time"],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        return redirect(url_for("admin"))

    rooms = []

    for room in room_docs:
        data = room.to_dict()
        status, next_available = get_status(room.id, timetable, demo_time, overrides)
        
        room_payload = {
            "id": room.id,
            "type": data.get("type"),
            "capacity": data.get("capacity"),
            "status": status,
            "next_available": next_available
        }

        if status == "Available":
            room_payload["density"] = get_camera_density()

        rooms.append(room_payload)

    return render_template("admin.html", rooms=rooms, demo_time=demo_time)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, host='0.0.0.0', port=port)