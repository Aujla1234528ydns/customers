"""
Customer Management System
Main Flask Application
"""
import pandas as pd

from reportlab.pdfgen import canvas

from flask import send_file

import os
from werkzeug.utils import secure_filename

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)
from database import get_connection
from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY


# ------------------------------
# Check Database Connection
# ------------------------------

try:
    connection = get_connection()
    connection.close()
    print("✅ Connected to MySQL Successfully!")

except Exception as e:
    print("❌ Database Connection Failed")
    print(e)


# ------------------------------
# Home Page
# ------------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/save_customer", methods=["POST"])
def save_customer():

    # -----------------------------
    # Connect to Database
    # -----------------------------

    connection = get_connection()

    cursor = connection.cursor()

    # -----------------------------
    # Read Form Data
    # -----------------------------

    full_name = request.form["full_name"]
    father_name = request.form["father_name"]
    mother_name = request.form["mother_name"]
    dob = request.form["dob"]
    gender = request.form["gender"]
    occupation = request.form["occupation"]
    mobile = request.form["mobile"]
    alternate_mobile = request.form["alternate_mobile"]
    email = request.form["email"]
    address = request.form["address"]
    city = request.form["city"]
    state = request.form["state"]
    pincode = request.form["pincode"]
    remarks = request.form["remarks"]
    photo = request.files["photo"]
    document = request.files["document"]

    photo_name = None
    document_name = None

# ----------------------------
# Upload Photo
# ----------------------------
    if photo and photo.filename != "":

        extension = photo.filename.rsplit(".", 1)[1].lower()

        ALLOWED_IMAGES = {"jpg", "jpeg", "png"}

        if extension in ALLOWED_IMAGES:

            photo_name = secure_filename(photo.filename)

            photo.save(
                os.path.join(
                    "static/uploads/photos",
                    photo_name
                        )
                    )

# ----------------------------
# Upload PDF
# ----------------------------
    if document and document.filename != "":

        extension = document.filename.rsplit(".", 1)[1].lower()

        if extension == "pdf":

            document_name = secure_filename(document.filename)

            document.save(
                os.path.join(
                    "static/uploads/documents",
                    document_name
                )
            )
    # -----------------------------
    # SQL Query
    # -----------------------------

    sql = """
    INSERT INTO customers
    (
        full_name,
        father_name,
        mother_name,
        dob,
        gender,
        occupation,
        mobile,
        alternate_mobile,
        email,
        address,
        city,
        state,
        pincode,
        remarks,
        photo,
        document
         )

    VALUES
    (
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
    )
    """

    values = (

        full_name,
        father_name,
        mother_name,
        dob,
        gender,
        occupation,
        mobile,
        alternate_mobile,
        email,
        address,
        city,
        state,
        pincode,
        remarks,
        photo_name,
        document_name

         )

    cursor.execute(sql, values)

    connection.commit()

    cursor.close()

    connection.close()

    return redirect(url_for("success"))
@app.route("/success")
def success():

    return render_template("success.html")
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(

        """
        SELECT *
        FROM admins
        WHERE username=%s
        AND password=%s
        """,

        (username,password)

        )

        admin = cursor.fetchone()

        cursor.close()

        connection.close()

        if admin:

            session["admin"] = username

            return redirect(url_for("dashboard"))

        else:

            return "Invalid Username or Password"

    return render_template("login.html")
@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor()

    # Total Customers
    cursor.execute("SELECT COUNT(*) FROM customers")
    total = cursor.fetchone()[0]

    # Today's Registrations
    cursor.execute("""
        SELECT COUNT(*)
        FROM customers
        WHERE DATE(created_at) = CURDATE()
    """)
    today = cursor.fetchone()[0]

    # Latest Customer
    cursor.execute("""
        SELECT full_name
        FROM customers
        ORDER BY created_at DESC
        LIMIT 1
    """)

    latest = cursor.fetchone()

    if latest:
        latest_name = latest[0]
    else:
        latest_name = "No Customer"

    cursor.close()
    connection.close()

    return render_template(
        "dashboard.html",
        total=total,
        today=today,
        latest=latest_name
    )
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")
@app.route("/customers")
def customers():

    if "admin" not in session:

        return redirect("/login")

    search = request.args.get("search")

    connection = get_connection()

    cursor = connection.cursor()

    if search:

        cursor.execute("""

        SELECT *

        FROM customers

        WHERE full_name LIKE %s

        OR mobile LIKE %s

        """,

        ("%"+search+"%",

        "%"+search+"%"))

    else:

        cursor.execute("SELECT * FROM customers")

    data = cursor.fetchall()

    cursor.close()

    connection.close()

    return render_template(

        "customers.html",

        customers=data

    )
@app.route("/edit/<int:id>")
def edit(id):

    if "admin" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM customers WHERE id=%s",
        (id,)
    )

    customer = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "edit.html",
        customer=customer
    )
@app.route("/update/<int:id>", methods=["POST"])
def update(id):

    if "admin" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor()

    sql = """
    UPDATE customers
    SET
    full_name=%s,
    father_name=%s,
    mother_name=%s,
    dob=%s,
    gender=%s,
    occupation=%s,
    mobile=%s,
    alternate_mobile=%s,
    email=%s,
    address=%s,
    city=%s,
    state=%s,
    pincode=%s,
    remarks=%s
    WHERE id=%s
    """

    values = (
        request.form["full_name"],
        request.form["father_name"],
        request.form["mother_name"],
        request.form["dob"],
        request.form["gender"],
        request.form["occupation"],
        request.form["mobile"],
        request.form["alternate_mobile"],
        request.form["email"],
        request.form["address"],
        request.form["city"],
        request.form["state"],
        request.form["pincode"],
        request.form["remarks"],
        id
    )

    cursor.execute(sql, values)

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/customers")
@app.route("/delete/<int:id>")
def delete(id):

    if "admin" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM customers WHERE id=%s",
        (id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/customers")
@app.route("/export_excel")
def export_excel():

    if "admin" not in session:
        return redirect("/login")

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
        id,
        full_name,
        mobile,
        email,
        city,
        state
        FROM customers
    """)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    df = pd.DataFrame(
        data,
        columns=[
            "ID",
            "Name",
            "Mobile",
            "Email",
            "City",
            "State"
        ]
    )

    file = "customers.xlsx"

    df.to_excel(file, index=False)

    return send_file(
        file,
        as_attachment=True
    )
@app.route("/export_pdf")
def export_pdf():

    if "admin" not in session:
        return redirect("/login")

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
        full_name,
        mobile,
        email
        FROM customers
    """)

    customers = cursor.fetchall()

    cursor.close()
    connection.close()

    filename = "customers.pdf"

    pdf = canvas.Canvas(filename)

    y = 800

    pdf.setFont("Helvetica-Bold",16)

    pdf.drawString(50,820,"Customer Report")

    pdf.setFont("Helvetica",11)

    for customer in customers:

        pdf.drawString(
            50,
            y,
            f"{customer[0]} | {customer[1]} | {customer[2]}"
        )

        y -= 20

        if y < 50:
            pdf.showPage()
            y = 800

    pdf.save()

    return send_file(
        filename,
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)