from flask import Flask, render_template, request, redirect, flash, url_for, send_file, session
import sqlite3
import os
from werkzeug.utils import secure_filename



app = Flask(__name__, template_folder='templates')
app.secret_key = "hello"

app.config['UPLOAD_FOLDER'] = "static//upload//"
path_of_file = 'G:/Haroon sir institute/E Learning/E-Learning-Flask/static/upload'

conn = sqlite3.connect('elearning.db', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS ss_registration (ID INTEGER PRIMARY KEY AUTOINCREMENT,REG_NO TEXT, FIRST_NAME TEXT, LAST_NAME TEXT, COURSE TEXT,SEM TEXT, EMAIL TEXT,PASSWORD TEXT, GENDER TEXT, PHONE INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS tregistration (ID INTEGER PRIMARY KEY AUTOINCREMENT,REG_NO TEXT, FIRST_NAME TEXT, LAST_NAME TEXT, EMAIL TEXT,PASSWORD TEXT, GENDER TEXT, PHONE INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS course (ID INTEGER PRIMARY KEY AUTOINCREMENT, COURSE_NAME TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS subject (ID INTEGER PRIMARY KEY AUTOINCREMENT, SUB_NAME TEXT, SEM TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS questionss (ID INTEGER PRIMARY KEY AUTOINCREMENT, C_NAME TEXT, S_NAME TEXT,T_NAME TEXT,STU_NAME TEXT,QUE TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS answers (ID INTEGER PRIMARY KEY AUTOINCREMENT, T_NAME TEXT, S_NAME TEXT, Q_NAME TEXT,ANS TEXT)")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/options")
def options():
    return render_template('options.html')


@app.route("/studentregistration", methods = ["GET", "POST"])
def studentregistration():
    if request.method == "POST":
        reg_no = request.form.get('reg_no')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        course = request.form.get('course')
        semester = request.form.get('sem')
        email = request.form.get('email')
        s_pass = request.form.get('s_pass')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        #print(first_name)
        #print(first_name, last_name, email, s_pass, gender, phone)
        print(course)
        c.execute("INSERT INTO ss_registration(REG_NO,FIRST_NAME, LAST_NAME,COURSE,SEM, EMAIL, PASSWORD, GENDER, PHONE) VALUES(?,?,?,?,?,?,?,?,?)",(reg_no,first_name, last_name,course,semester, email, s_pass, gender, phone))
        conn.commit()
        flash("Registered successfully...!")
        return render_template('studentlogin.html')

    c.execute("SELECT * FROM course")
    rows = c.fetchall()

    c.execute("SELECT * FROM semester")
    s_rows = c.fetchall()
    return render_template('studentregistration.html', rows=rows, s_rows=s_rows)

@app.route("/studentlogin", methods = ["GET", "POST"])
def studentlogin():
    if request.method == "POST":
        email = request.form.get('email')
        session["student_user"] = email
        s_pass = request.form.get('s_pass')
        conn = sqlite3.connect('elearning.db', check_same_thread=False)
        c = conn.cursor()
        statement = f"SELECT * FROM ss_registration WHERE EMAIL='{email}' AND PASSWORD='{s_pass}'"
        c.execute(statement)
        if not c.fetchone():
            record = c.fetchone()
            session["name"] = record
            flash("Username/Password incorrect...!")
            return render_template('studentlogin.html')
        else:
            flash("Login Successfully...!")
            return render_template('studenthome.html')

    return render_template('studentlogin.html')


@app.route("/chat", methods = ["GET", "POST"])
def chat():

    return render_template("chat.html")


@app.route("/addcourse", methods = ["GET", "POST"])
def addcourse():
    if request.method == "POST":
        course = request.form.get('course')
        statement = f"INSERT INTO course(COURSE_NAME) VALUES('{course}')"
        c.execute(statement)
        conn.commit()
        return redirect(url_for('adminhome'))
    return render_template("addcourse.html")

@app.route("/showcourse")
def showcourse():
    c.execute("SELECT * FROM course")
    rows = c.fetchall()
    return render_template('showcourse.html', rows=rows)



@app.route("/deletecourse/<string:record_id>", methods = ["POST", "GET"])
def deletecourse(record_id):
    try:
        c.execute("DELETE FROM course WHERE ID=?",(record_id))
        conn.commit()
        flash("Record Deleted Successfully", "success")

    except:
        flash("Record Delete Failed", "danger")
    finally:
        return redirect(url_for('showcourse'))


@app.route("/addsubject", methods = ["GET", "POST"])
def addsubject():
    if request.method == "POST":
        subject = request.form.get('subject')
        sem = request.form.get('sem')
        c.execute("INSERT INTO subject(SUB_NAME, SEM) VALUES(?,?)", (subject, sem))
        conn.commit()
        return redirect(url_for('adminhome'))
    return render_template("addsubject.html")

@app.route("/showsubject")
def showsubject():
    c.execute("SELECT * FROM subject")
    rows = c.fetchall()
    return render_template('showsubject.html', rows=rows)


@app.route("/teacherregistration", methods = ["GET", "POST"])
def teacherregistration():
    if request.method == "POST":
        reg_no = request.form.get('reg_no')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        s_pass = request.form.get('s_pass')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        #print(first_name)
        #print(first_name, last_name, email, s_pass, gender, phone)
        c.execute("INSERT INTO tregistration(REG_NO,FIRST_NAME, LAST_NAME, EMAIL, PASSWORD, GENDER, PHONE) VALUES(?,?,?,?,?,?,?)",(reg_no,first_name, last_name, email, s_pass, gender, phone))
        conn.commit()
        flash("Registered successfully...!")
    return  render_template('teacherregistration.html')



@app.route("/teacherlogin", methods = ["GET", "POST"])
def teacherlogin():
    if request.method == "POST":
        t_email = request.form.get('email')
        session["teacher_email"] = t_email
        s_pass = request.form.get('s_pass')
        conn = sqlite3.connect('elearning.db', check_same_thread=False)
        c = conn.cursor()
        statement = f"SELECT * FROM tregistration WHERE EMAIL='{t_email}' AND PASSWORD='{s_pass}'"
        c.execute(statement)
        if not c.fetchone():
            flash("Username/Password incorrect...!")
            return render_template('teacherlogin.html')
        else:
            record = c.fetchone()
            flash("Login Successfully...!")
            return render_template('teacherhome.html', record=record)

    return  render_template('teacherlogin.html')


@app.route("/adminlogin", methods = ["GET", "POST"])
def adminlogin():
    if request.method == "POST":
        u_name = request.form.get('user_name')
        session["admin_user"] = u_name
        p_word = request.form.get('s_pass')

        admin = 'admin'
        password = 'admin123'

        if(u_name != admin) and (p_word != password):
            flash("Username/Password incorrect...!")
            return render_template('adminlogin.html')
        else:
            flash("Login Successfully...!")
            return render_template('adminhome.html')
    return render_template('adminlogin.html')

@app.route("/studenthome")
def studenthome():
    return render_template('studenthome.html')

@app.route("/adminhome")
def adminhome():
    return render_template('adminhome.html')


@app.route("/studentdetails")
def studentdetails():
    c.execute("SELECT * FROM ss_registration")
    rows = c.fetchall()
    return render_template('studentdetails.html', rows = rows)

@app.route("/deletestudent/<string:record_id>", methods = ["POST", "GET"])
def deletestudent(record_id):
    try:
        c.execute("DELETE FROM ss_registration WHERE ID=?",(record_id))
        conn.commit()
        flash("Record Deleted Successfully", "success")

    except:
        flash("Record Delete Failed", "danger")
    finally:
        return redirect(url_for('studentdetails'))


@app.route("/deleteteacher/<string:record_id>", methods = ["POST", "GET"])
def deleteteacher(record_id):
    try:
        c.execute("DELETE FROM tregistration WHERE ID=?",(record_id))
        conn.commit()
        flash("Record Deleted Successfully", "success")

    except:
        flash("Record Delete Failed", "danger")
    finally:
        return redirect(url_for('teacherdetails'))

@app.route("/teacherdetials")
def teacherdetails():
    c.execute("SELECT * FROM tregistration")
    rows = c.fetchall()
    return render_template('teacherdetails.html', rows = rows)


@app.route("/documentdetails")
def documentdetails():
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template('documentdetails.html', files=files)


@app.route("/teacherhome", methods=["POST", "GET"])
def teacherhome():
    return render_template('teacherhome.html')

@app.route("/uploaddoc", methods=["POST", "GET"])
def uploaddoc():
    if request.method == "POST":
        #if 'file' not in request.files:
            #print('No File')
            #return redirect(url_for('teacherhome'))
        file = request.files["customFile"]
        #if file.filename == '':
            #print('No Filename')
            #return redirect(url_for('teacherhome'))
        #else:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('teacherhome'))
    return render_template('teacherhome.html')


@app.route("/listfiles")
def listfiles():
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template('teacherhome.html', files = files)

@app.route("/slistfiles")
def slistfiles():
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template('studenthome.html', files = files)

@app.route("/dlistfiles")
def dlistfiles():
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template('documentdetails.html', files = files)

@app.route("/returnfiles/<file>")
def returnfiles(file):
    filepath = app.config['UPLOAD_FOLDER'] + file
    return send_file(filepath, as_attachment = True, attachment_filename='')


@app.route("/library")
def library():
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("library.html", files = files)




@app.route("/questions", methods=["GET", "POST"])
def questions():
    if request.method == "POST":
        course = request.form.get("course")
        subject = request.form.get("subject")
        teacher = request.form.get("teacher")
        que = request.form.get("ques")

        if 'student_user' in session:
            user = session['student_user']
            c.execute("SELECT FIRST_NAME FROM ss_registration WHERE EMAIL=?", [user])
            conn.commit()
            name = c.fetchone()
            actual_name = name[0]
            c.execute("INSERT INTO questionss(C_NAME, S_NAME, T_NAME,STU_NAME, QUE) VALUES(?,?,?,?,?)",(course, subject, teacher, actual_name, que))
            conn.commit()

    c.execute("SELECT * FROM course")
    c_rows = c.fetchall()

    c.execute("SELECT * FROM subject")
    s_rows = c.fetchall()

    c.execute("SELECT * FROM tregistration")
    t_rows = c.fetchall()

    return render_template("questions.html", c_rows=c_rows, s_rows=s_rows, t_rows=t_rows)




@app.route("/answers", methods=["POST", "GET"])
def answers():
    if request.method == "POST":
        tea_name = request.form.get('tea_name')
        stu_name = request.form.get('stu_name')
        que_name = request.form.get('que_name')
        answer_s = request.form.get('answer')

        c.execute("INSERT INTO answers(T_NAME,S_NAME,Q_NAME,ANS) VALUES(?,?,?,?)", (tea_name, stu_name, que_name, answer_s))
        conn.commit()
        return redirect(url_for('allqs'))

    c.execute("SELECT * FROM questionss")
    record = c.fetchall()

    c.execute("SELECT * FROM tregistration")
    t_record = c.fetchall()
    return render_template("answers.html",stu_name=record, t_record=t_record)






@app.route("/displayquestions", methods=["POST", "GET"])
def displayquestions():
    c.execute("SELECT * FROM questionss")
    rows = c.fetchall()
    return render_template("displayquestions.html", rows = rows)


@app.route("/allanswers")
def allanswers():
    c.execute("SELECT * FROM answers")
    rows = c.fetchall()
    return render_template("allanswers.html", rows = rows)



@app.route("/showquestions")
def showquestions():
    c.execute("SELECT * FROM questionss")
    rows = c.fetchall()
    return render_template('showquestions.html', rows=rows)



@app.route("/deletequestions/<string:record_id>", methods = ["POST", "GET"])
def deletequestions(record_id):
    try:
        c.execute("DELETE FROM questionss WHERE ID=?",(record_id))
        conn.commit()
        flash("Record Deleted Successfully", "success")

    except:
        flash("Record Delete Failed", "danger")
    finally:
        return redirect(url_for('showquestions'))



@app.route("/showanswers")
def showanswers():
    c.execute("SELECT * FROM answers")
    rows = c.fetchall()
    return render_template('showanswers.html', rows=rows)



@app.route("/deleteanswers/<string:record_id>", methods = ["POST", "GET"])
def deleteanswers(record_id):
    try:
        c.execute("DELETE FROM answers WHERE ID=?",(record_id))
        conn.commit()
        flash("Record Deleted Successfully", "success")

    except:
        flash("Record Delete Failed", "danger")
    finally:
        return redirect(url_for('showanswers'))



@app.route("/studentlogout")
def studentlogout():
    session.pop("student_user", None)
    return render_template("options.html")




@app.route("/teacherlogout")
def teacherlogout():
    session.pop("teacher_email", None)
    return render_template("options.html")


@app.route("/adminlogout")
def adminlogout():
    session.pop("admin_user", None)
    return render_template("options.html")




@app.route("/libraryt")
def libraryt():
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("libraryt.html", files=files)

@app.route("/allqs")
def allqs():
    c.execute("SELECT * FROM answers")
    conn.commit()
    qdata = c.fetchall()
    return render_template("allquestionanswers.html", qdata = qdata)


if __name__ == "__main__":
    app.run(debug=True)