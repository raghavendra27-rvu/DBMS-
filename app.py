import os
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "student_record_secret"

# MySQL database connection
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "1234",
    "database": "student_db"
}

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)


# Display all students and search students
@app.route("/")
def index():
    search = request.args.get("q", "").strip()
    conn = None

    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)

        if search:
            value = "%" + search + "%"
            cursor.execute(
                """SELECT * FROM students
                WHERE name LIKE %s OR email LIKE %s OR course LIKE %s
                ORDER BY student_id DESC""",
                (value, value, value)
            )
        else:
            cursor.execute(
                "SELECT * FROM students ORDER BY student_id DESC"
            )

        students = cursor.fetchall()
        cursor.close()

        return render_template(
            "index.html",
            students=students,
            q=search
        )

    except Error as e:
        return "Database Error: " + str(e)

    finally:
        if conn and conn.is_connected():
            conn.close()


# Add student
@app.route("/add", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        course = request.form["course"].strip()
        semester = request.form["semester"].strip()

        if not name or not email or not course or not semester:
            flash("Please fill all fields.")
            return redirect(url_for("add_student"))

        try:
            semester = int(semester)
            if semester < 1 or semester > 12:
                raise ValueError
        except ValueError:
            flash("Semester must be between 1 and 12.")
            return redirect(url_for("add_student"))

        conn = None
        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO students
                (name, email, course, semester)
                VALUES (%s, %s, %s, %s)""",
                (name, email, course, semester)
            )

            conn.commit()
            cursor.close()

            flash("Student added successfully!")
            return redirect(url_for("index"))

        except Error as e:
            flash("Error: " + str(e))
        finally:
            if conn and conn.is_connected():
                conn.close()

    return render_template("index.html", student={}, form_mode=True)


# Update student
@app.route("/edit/<int:sid>", methods=["GET", "POST"])
def edit_student(sid):
    conn = None
    cursor = None

    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)

        if request.method == "POST":
            name = request.form["name"].strip()
            email = request.form["email"].strip()
            course = request.form["course"].strip()

            try:
                semester = int(request.form["semester"])
            except ValueError:
                flash("Semester must be a number.")
                return redirect(url_for("edit_student", sid=sid))

            if not name or not email or not course:
                flash("Please fill all fields.")
                return redirect(url_for("edit_student", sid=sid))

            if semester < 1 or semester > 12:
                flash("Semester must be between 1 and 12.")
                return redirect(url_for("edit_student", sid=sid))

            cursor.execute(
                """UPDATE students
                SET name=%s, email=%s, course=%s, semester=%s
                WHERE student_id=%s""",
                (name, email, course, semester, sid)
            )

            conn.commit()
            flash("Student updated successfully!")
            return redirect(url_for("index"))

        cursor.execute(
            "SELECT * FROM students WHERE student_id=%s",
            (sid,)
        )

        student = cursor.fetchone()

        if student is None:
            flash("Student not found.")
            return redirect(url_for("index"))

        return render_template(
            "form.html",
            student=student,
            heading="Edit Student"
        )

    except Error as e:
        flash("Database Error: " + str(e))
        return redirect(url_for("index"))

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

     # Delete student
@app.route("/delete/<int:sid>", methods=["POST"])
def delete_student(sid):
    conn = None

    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM students WHERE student_id=%s",
            (sid,)
        )

        conn.commit()
        cursor.close()

        flash("Student deleted successfully!")

    except Error as e:
        flash("Database Error: " + str(e))

    finally:
        if conn and conn.is_connected():
            conn.close()

    return redirect(url_for("index"))
# Run the application
if __name__ == "__main__":
    app.run(debug=True)       