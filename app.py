from flask import Flask, render_template, request, send_file
from datetime import datetime
import csv
import os

app = Flask(__name__)

START_TIME = "14:00"
END_TIME = "15:00"

FILE = "attendance.csv"

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    students = []

    if request.method == "POST":
        roll = request.form["roll"]
        current_time = datetime.now().strftime("%H:%M")

        if START_TIME <= current_time <= END_TIME:

            duplicate = False
            if os.path.exists(FILE):
                with open(FILE, "r") as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row[0] == roll:
                            duplicate = True
                            message = "Attendance already marked"

            if not duplicate:
                with open(FILE, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([roll, current_time])
                message = "Attendance Marked Successfully"

        else:
            message = "Attendance Closed"

    return render_template("index.html", message=message)


@app.route("/dashboard")
def dashboard():
    students = []

    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            reader = csv.reader(f)
            students = list(reader)

    return render_template("dashboard.html", students=students)


@app.route("/download")
def download():
    return send_file(FILE, as_attachment=True)


app.run(host="0.0.0.0", port=5000)