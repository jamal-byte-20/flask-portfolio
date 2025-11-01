from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
import sqlite3
import os
from service import Service
from project import Project
from flask_mail import Mail, Message
from validate_email_address import validate_email

app = Flask(__name__)
app.secret_key = "@jk2006@"
USER = "jamal"
PASSWORD = "2006"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'     # or your mail server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "kerroujamal54@gmail.com"     # your Gmail
app.config['MAIL_PASSWORD'] = "dazy kbit hcdd fwnu"        # your Gmail app password
app.config['MAIL_DEFAULT_SENDER'] = "kerroujamal54@gmail.com"

def get_db():
    try:
        conn = sqlite3.connect("data.db")
    except Exception as e:
        print(e)
    conn.row_factory = sqlite3.Row
    return conn

def testSession():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('admin_login'))
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('admin_login'))
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('admin_login'))

#-------------------client---------------------------#
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/whoiam")
def whoiam():
    return render_template("whoiam.html") 

@app.route("/projects")
def project():
    conn = get_db()
    c = conn.cursor()
    projects = c.execute("SELECT * FROM project;").fetchall()
    return render_template("projects.html", projects = projects)

@app.route("/services")
def services():
    conn = get_db()
    c = conn.cursor()
    services = c.execute("SELECT * FROM services;").fetchall()
    return render_template("services.html", services = services)

@app.route("/contact")
def contact():
    return render_template("contact.html") 


#-------------------admin---------------------------#
@app.route('/admin')
def admin():
   if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('admin_dashbord'))
   return redirect(url_for('admin_login'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USER and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin_dashbord'))
        else:
            flash("you'r not admin", 'error')
    return render_template('admin/login.html')

@app.route('/admin/dashbord')
def admin_dashbord():
    if 'logged_in' in session and session['logged_in']:
        return render_template('admin/dashbord.html')
    return redirect(url_for('admin_login'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin_login'))

#---------services management------------------#

@app.route("/admin/sermanage")
def sermanage():

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services;")
    services = cursor.fetchall()
    if 'logged_in' in session and session['logged_in']:
        return render_template("admin/sermanage.html",services = services)
    return redirect(url_for('admin_login'))
#search------------------
@app.route('/admin/search_service', methods=['GET'])
def search_services():
    sername = f"%{request.args.get('sername')}%"
    try:
        servs = Service.getService(sername)
        return jsonify(servs)
    except Exception as e:
        return jsonify({"error": str(e)}),500

#add service-----------
@app.route("/admin/addService",methods=['POST'])
def addService():
    testSession()
    t = request.form.get("title")
    d= request.form.get("description")
    img = request.files.get("img")
    Service.addService(t,d,img)
    return redirect("/admin/sermanage")

#delet service------------
@app.route("/admin/delete_service")
def delete_service():
    testSession()
    id = request.args.get("id")
    conn = sqlite3.connect("data.db")
    Service.removeService(id)
    return redirect("/admin/sermanage")

#edit service---------------    
@app.route("/admin/editService", methods=['POST'])
def edService():
    testSession()
    id = request.form.get("id")
    title = request.form.get("title")
    description = request.form.get("description")
    newimg = request.files.get("img")
    Service.updateService(id,title,description,newimg)
    return redirect("/admin/sermanage")


#----------projects managment----------#
@app.route("/admin/projmanage")
def projmanage():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM project;")
    projects = cursor.fetchall()
    if 'logged_in' in session and session['logged_in']:
        return render_template("admin/projmanage.html",projects = projects)
    return redirect(url_for('admin_login'))

#search project---------------------    
@app.route('/admin/search_projects', methods=['GET'])
def search_projects():
    projname = f"%{request.args.get('projname')}%"
    try:
        projects = Project.getProject(projname)
        return jsonify(projects)
    except Exception as e:
        return jsonify({"error": str(e)})

#add project-----------------------
@app.route("/admin/addProject",methods=['POST'])
def addProject():
    testSession()
    t = request.form.get("title")
    d= request.form.get("description")
    img = request.files.get("img")
    link = request.form.get("link")
    Project.addProject(img,t,d,link)
    return redirect("/admin/projmanage")

#delet project------------
@app.route("/admin/delete_project")
def delete_project():
    testSession()
    id = request.args.get("id")
    Project.removeProject(id)
    return redirect("/admin/projmanage")


#edit project---------------    
@app.route("/admin/editeProject", methods=['POST'])
def edProject():
    testSession()
    id = request.form.get("id")
    title = request.form.get("title")
    description = request.form.get("description")
    link = request.form.get("link")
    newimg = request.files.get("img")
    Project.updateProject(id,title,description,link,newimg)
    return redirect("/admin/projmanage")


mail = Mail(app)
@app.route('/SendMessage', methods=['GET', 'POST'])
def SendMsg():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        if not validate_email(email, verify=False):
            flash("❌ Invalid email address.", "danger")
            return redirect(url_for('contact'))
        msg = Message(
            subject=f"New message from {name}",
            recipients=[app.config['MAIL_USERNAME']],
            body=f"From: {name} <{email}>\n\nMessage:\n{message}"
        )

        try:
            mail.send(msg)
            flash("✅ Message sent successfully!", "success")
            return redirect(url_for('contact'))
        except Exception as e:
            print("❌ Error sending email:", e)
            flash("❌ Something went wrong. Please try again.", "danger")

    return render_template('contact.html')





if __name__ == '__main__':
    app.run(debug=True)