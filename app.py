from typing import Any
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

import flask
app = Flask(__name__)
db_locale = 'student.db'
@app.route('/')
def hello_world():
    return render_template('login.html')
@app.route("/form_login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email1 = request.form['email']
        password1 = request.form['password']
        db_locale = "student.db"
        conn = sqlite3.connect(db_locale)
        #conn.row_factory = sqlite3.Row
        c = conn.cursor()
        data = c.fetchall()
        substr1="@ssn.edu.in"
        substr2="@it.ssn.edu.in"
        if email1.find(substr1) !=-1:
            post = conn.execute('SELECT mail,password FROM login WHERE mail = ? and password = ?',
                            (email1,password1)).fetchone()
            name = conn.execute('SELECT name FROM users where mail = ? and password = ?', (email1, password1)).fetchone()
            course = conn.execute('SELECT sub1_name,sub2_name,sub3_name FROM users WHERE mail = ? and password = ?',
                            (email1, password1)).fetchone()
            role = conn.execute('SELECT role FROM users WHERE mail = ? and password = ?',
                            (email1, password1)).fetchone()
            if post:
                for i in role:
                    if i == "class_advisor":
                        return render_template("classs_advisor.html", name=name, course=course)
                    elif i =="Course Instructor":
                        return render_template("course_instructor.html", name=name, course=course)
                    elif i == "Mentor":
                        return render_template("mentor1.html",name =name)
                    else:
                        return render_template("hod.html",name=name)
            else:
                error= 'Invalid credentials. Please try again'
        elif email1.find(substr2) != -1:
            n = len(data)
            r = c.fetchone()
            t= conn.cursor()
            reg_no1 = t.execute('SELECT reg_no,name FROM student_details WHERE email = ? and password =?',(email1,password1)).fetchone()
            name1 = t.execute('SELECT name FROM student_details WHERE email = ? and password =?',(email1,password1)).fetchone()
            post = conn.execute('SELECT email,password FROM student_details WHERE email = ? and password = ?',
                                 (email1,password1)).fetchone()
            (reg_no,name2)=reg_no1
            if post:
                data.append(reg_no)
                data.append(name2)
                return redirect(url_for('home_page',data =data))
            else:
                error= 'Invalid credentials. Please try again'
        
        conn.commit()
        conn.close()
    return render_template('login.html',error=error)
@app.route('/editatt/<cname>')
def edit_attt(cname):
    course1=cname
    return render_template('edit_att.html',course1=course1)


@app.route('/home/<data>',methods =['GET','POST'])

def home_page(data):
    if request.method == 'GET':
        tx=""
        for i in range(1,10):
            tx+=data[i]
        reg=int(tx)
        conn=sqlite3.connect(db_locale)
        c=conn.cursor()
        sql_execute_string = 'SELECT name FROM student_details WHERE reg_no = ?'
        c.execute(sql_execute_string,[reg])
        conn.commit()
        name=c.fetchall()
        name=name[0][0]
        student_data = query_contact_details() 
        return render_template('student_index.html',student_data=student_data,data =data,reg=reg,name=name)

def add_remarks(remark_details):
    conn=sqlite3.connect(db_locale)
    c=conn.cursor()
    sql_execute_string = 'INSERT INTO Remarks (reg_no,name,email,Subject_Code,Recipient,Remark) VALUES (?,?,?,?,?,?)'
    c.execute(sql_execute_string,remark_details)
    conn.commit()
    conn.close()
def query_contact_details():
    conn=sqlite3.connect(db_locale)
    c=conn.cursor()
    c.execute("""
    SELECT * FROM student_details
    """)
    student_data=c.fetchall()
    return student_data
@app.route('/remarks/<remarksdata>',methods = ['GET','POST'])
def remarks(remarksdata):
    if request.method == 'GET':
        student_data = query_contact_details() 
        return render_template('remarks.html',remarksdata=remarksdata)
    else:
        remark_details = (
            request.form['reg_no'],
            request.form['name'],
            request.form['email'],
            request.form['subject'],
            request.form['recipient'],
            request.form['remark']
        )
        add_remarks(remark_details)
        return render_template('remarks_success.html',remarksdata=remarksdata)

def add_remarks(remark_details):
    conn=sqlite3.connect(db_locale)
    c=conn.cursor()
    sql_execute_string = 'INSERT INTO Remarks (reg_no,name,email,Subject_Code,Recipient,Remark) VALUES (?,?,?,?,?,?)'
    c.execute(sql_execute_string,remark_details)
    conn.commit()
    conn.close()
@app.route('/od_request/<oddata>',methods = ['GET','POST'])
def od_page(oddata):
    if request.method == 'GET':
        reg=oddata[0]
        name=oddata[1]
        return render_template('od_page.html',oddata=oddata)
    else:
        od_details = (
            request.form['reg_no'],
            request.form['name'],
            request.form['date'],
            request.form['course'],
            request.form['link']
        )
        reg=oddata[0]
        name=oddata[1]
        add_od(od_details)
        return render_template('od_success.html',oddata=oddata)
def add_od(od_details):
    conn=sqlite3.connect(db_locale)
    c=conn.cursor()
    sql_execute_string = 'INSERT INTO OD_Request (reg_no,name,date,course,link) VALUES (?,?,?,?,?)'
    c.execute(sql_execute_string,od_details)
    conn.commit()
    conn.close()

@app.route('/attendance/<data>',methods = ['GET','POST'])
def att_page(data):
    if request.method == 'GET':
        return render_template('attendance_choose.html',data = data)
    else:
        choice=(
            request.form['course'],
            request.form['period']        
        )
        reg=data
        if choice[0] == 'fat':
            if choice[1] == 'cat1':
                (att_data,att_desc,tot_att)=att_from_db(choice,reg)
                return render_template('student_attendance_page.html',choice=choice,att_data=att_data,att_desc=att_desc,tot_att = tot_att)
            elif choice[1] == 'cat2':
                (att_data,att_desc,tot_att)=att_from_db(choice,reg)
                return render_template('student_attendance_page.html',choice=choice,att_data=att_data,att_desc=att_desc,tot_att=tot_att)
            else:
                (att_data,att_desc,tot_att)=att_from_db(choice,reg)
                return render_template('student_attendance_page.html',choice=choice,att_data=att_data,att_desc=att_desc,tot_att=tot_att)
        elif choice[0] == 'pos':
            if choice[1] == 'cat1':
                (att_data,att_desc,tot_att)=att_from_db(choice,reg)
                return render_template('student_attendance_page.html',choice=choice,att_data=att_data,att_desc=att_desc,tot_att=tot_att)
            elif choice[1] == 'cat2':
                (att_data,att_desc,tot_att)=att_from_db(choice,reg)
                return render_template('student_attendance_page.html',choice=choice,att_data=att_data,att_desc=att_desc,tot_att=tot_att)
            else:
                (att_data,att_desc,tot_att)=att_from_db(choice,reg)
                return render_template('student_attendance_page.html',choice=choice,att_data=att_data,att_desc=att_desc,tot_att=tot_att)
        elif choice[0] == 'cna':
            if choice[1] == 'cat1':
                (att_data,att_desc,tot_att)=att_from_db(choice,reg)
                return render_template('student_attendance_page.html',choice=choice,att_data=att_data,att_desc=att_desc,tot_att=tot_att)
            elif choice[1] == 'cat2':
                (att_data,att_desc,tot_att)=att_from_db(choice,reg)
                return render_template('student_attendance_page.html',choice=choice,att_data=att_data,att_desc=att_desc,tot_att=tot_att)
            else:
                (att_data,att_desc,tot_att)=att_from_db(choice,reg)
                return render_template('student_attendance_page.html',choice=choice,att_data=att_data,att_desc=att_desc,tot_att=tot_att)
        elif choice[0] == 'idsp':
            if choice[1] == 'cat1':
                (att_data,att_desc,tot_att)=att_from_db(choice,reg)
                return render_template('student_attendance_page.html',choice=choice,att_data=att_data,att_desc=att_desc,tot_att=tot_att)
            elif choice[1] == 'cat2':
                (att_data,att_desc,tot_att)=att_from_db(choice,reg)
                return render_template('student_attendance_page.html',choice=choice,att_data=att_data,att_desc=att_desc,tot_att=tot_att)
            else:
                (att_data,att_desc,tot_att)=att_from_db(choice,reg)
                return render_template('student_attendance_page.html',choice=choice,att_data=att_data,att_desc=att_desc,tot_att=tot_att)
        elif choice[0] == 'aica':
            if choice[1] == 'cat1':
                (att_data,att_desc,tot_att)=att_from_db(choice,reg)
                return render_template('student_attendance_page.html',choice=choice,att_data=att_data,att_desc=att_desc,tot_att=tot_att)
            elif choice[1] == 'cat2':
                (att_data,att_desc,tot_att)=att_from_db(choice,reg)
                return render_template('student_attendance_page.html',choice=choice,att_data=att_data,att_desc=att_desc,tot_att=tot_att)
            else:
                (att_data,att_desc,tot_att)=att_from_db(choice,reg)
                return render_template('student_attendance_page.html',choice=choice,att_data=att_data,att_desc=att_desc,tot_att=tot_att)
        elif choice[0] == 'fdip':
            if choice[1] == 'cat1':
                (att_data,att_desc,tot_att)=att_from_db(choice,reg)
                return render_template('student_attendance_page.html',choice=choice,att_data=att_data,att_desc=att_desc,tot_att=tot_att)
            elif choice[1] == 'cat2':
                (att_data,att_desc,tot_att)=att_from_db(choice,reg)
                return render_template('student_attendance_page.html',choice=choice,att_data=att_data,att_desc=att_desc,tot_att=tot_att)
            else:
                (att_data,att_desc,tot_att)=att_from_db(choice,reg)
                return render_template('student_attendance_page.html',choice=choice,att_data=att_data,att_desc=att_desc,tot_att=tot_att)
        elif choice[0] == 'dc':
            if choice[1] == 'cat1':
                (att_data,att_desc,tot_att)=att_from_db(choice,reg)
                return render_template('student_attendance_page.html',choice=choice,att_data=att_data,att_desc=att_desc,tot_att=tot_att)
            elif choice[1] == 'cat2':
                (att_data,att_desc,tot_att)=att_from_db(choice,reg)
                return render_template('student_attendance_page.html',choice=choice,att_data=att_data,att_desc=att_desc,tot_att=tot_att)
            else:
                (att_data,att_desc,tot_att)=att_from_db(choice,reg)
                return render_template('student_attendance_page.html',choice=choice,att_data=att_data,att_desc=att_desc,tot_att=tot_att)
def att_from_db(choice,reg_no):
    x2=reg_no
    if choice[0] == 'fat':
        if choice[1] == 'cat1':
            sql_ex_str = 'SELECT * FROM Attendance_fat_cat1 WHERE reg_no = ?'
            sql_ex_str2 ='SELECT Class1 + Class2 + Class3 + Class4+ Class5 +Class6 + Class7 as TOTAL_ATT FROM Attendance_fat_cat1 WHERE reg_no = ?'
        elif choice[1] == 'cat2':
            sql_ex_str = 'SELECT * FROM Attendance_fat_cat2 WHERE reg_no = ?'
            sql_ex_str2 ='SELECT Class1 + Class2 + Class3 + Class4+ Class5 +Class6 + Class7 as TOTAL_ATT FROM Attendance_fat_cat1 WHERE reg_no = ?'
        else:
            sql_ex_str = 'SELECT * FROM Attendance_fat_cat3 WHERE reg_no = ?'
            sql_ex_str2 ='SELECT Class1 + Class2 + Class3 + Class4+ Class5 +Class6 + Class7 as TOTAL_ATT FROM Attendance_fat_cat1 WHERE reg_no = ?'
    elif choice[0] == 'pos':
        if choice[1] == 'cat1':
            sql_ex_str = 'SELECT * FROM Attendance_pos_cat1 WHERE reg_no = ?'
            sql_ex_str2 ='SELECT Class1 + Class2 + Class3 + Class4+ Class5 +Class6 + Class7 as TOTAL_ATT FROM Attendance_pos_cat1 WHERE reg_no = ?'
        elif choice[1] == 'cat2':
            sql_ex_str = 'SELECT * FROM Attendance_pos_cat2 WHERE reg_no = ?'
            sql_ex_str2 ='SELECT Class1 + Class2 + Class3 + Class4+ Class5 +Class6 + Class7 as TOTAL_ATT FROM Attendance_pos_cat2 WHERE reg_no = ?'
        else:
            sql_ex_str = 'SELECT * FROM Attendance_pos_cat3 WHERE reg_no = ?'
            sql_ex_str2 ='SELECT Class1 + Class2 + Class3 + Class4+ Class5 +Class6 + Class7 as TOTAL_ATT FROM Attendance_pos_cat3 WHERE reg_no = ?'
    elif choice[0] == 'cna':
        if choice[1] == 'cat1':
            sql_ex_str = 'SELECT * FROM Attendance_cna_cat1 WHERE reg_no = ?'
            sql_ex_str2 ='SELECT Class1 + Class2 + Class3 + Class4+ Class5 +Class6 + Class7 as TOTAL_ATT FROM Attendance_cna_cat1 WHERE reg_no = ?'
        elif choice[1] == 'cat2':
            sql_ex_str = 'SELECT * FROM Attendance_cna_cat2 WHERE reg_no = ?'
            sql_ex_str2 ='SELECT Class1 + Class2 + Class3 + Class4+ Class5 +Class6 + Class7 as TOTAL_ATT FROM Attendance_cna_cat2 WHERE reg_no = ?'
        else:
            sql_ex_str = 'SELECT * FROM Attendance_cna_cat3 WHERE reg_no = ?'
            sql_ex_str2 ='SELECT Class1 + Class2 + Class3 + Class4+ Class5 +Class6 + Class7 as TOTAL_ATT FROM Attendance_cna_cat3 WHERE reg_no = ?'
    elif choice[0] == 'idsp':
        if choice[1] == 'cat1':
            sql_ex_str = 'SELECT * FROM Attendance_idsp_cat1 WHERE reg_no = ?'
            sql_ex_str2 ='SELECT Class1 + Class2 + Class3 + Class4+ Class5 +Class6 + Class7 as TOTAL_ATT FROM Attendance_idsp_cat1 WHERE reg_no = ?'
        elif choice[1] == 'cat2':
            sql_ex_str = 'SELECT * FROM Attendance_idsp_cat2 WHERE reg_no = ?'
            sql_ex_str2 ='SELECT Class1 + Class2 + Class3 + Class4+ Class5 +Class6 + Class7 as TOTAL_ATT FROM Attendance_idsp_cat2 WHERE reg_no = ?'
        else:
            sql_ex_str = 'SELECT * FROM Attendance_idsp_cat3 WHERE reg_no = ?'
            sql_ex_str2 ='SELECT Class1 + Class2 + Class3 + Class4+ Class5 +Class6 + Class7 as TOTAL_ATT FROM Attendance_idsp_cat3 WHERE reg_no = ?'
    elif choice[0] == 'aica':
        if choice[1] == 'cat1':
            sql_ex_str = 'SELECT * FROM Attendance_aica_cat1 WHERE reg_no = ?'
            sql_ex_str2 ='SELECT Class1 + Class2 + Class3 + Class4+ Class5 +Class6 + Class7 as TOTAL_ATT FROM Attendance_aica_cat1 WHERE reg_no = ?'
        elif choice[1] == 'cat2':
            sql_ex_str = 'SELECT * FROM Attendance_aica_cat2 WHERE reg_no = ?'
            sql_ex_str2 ='SELECT Class1 + Class2 + Class3 + Class4+ Class5 +Class6 + Class7 as TOTAL_ATT FROM Attendance_aica_cat2 WHERE reg_no = ?'
        else:
            sql_ex_str = 'SELECT * FROM Attendance_aica_cat3 WHERE reg_no = ?'
            sql_ex_str2 ='SELECT Class1 + Class2 + Class3 + Class4+ Class5 +Class6 + Class7 as TOTAL_ATT FROM Attendance_aica_cat3 WHERE reg_no = ?'
    elif choice[0] == 'fdip':
        if choice[1] == 'cat1':
            sql_ex_str = 'SELECT * FROM Attendance_fdip_cat1 WHERE reg_no = ?'
            sql_ex_str2 ='SELECT Class1 + Class2 + Class3 + Class4+ Class5 +Class6 + Class7 as TOTAL_ATT FROM Attendance_fdip_cat1 WHERE reg_no = ?'
        elif choice[1] == 'cat2':
            sql_ex_str = 'SELECT * FROM Attendance_fdip_cat2 WHERE reg_no = ?'
            sql_ex_str2 ='SELECT Class1 + Class2 + Class3 + Class4+ Class5 +Class6 + Class7 as TOTAL_ATT FROM Attendance_fdip_cat2 WHERE reg_no = ?'
        else:
            sql_ex_str = 'SELECT * FROM Attendance_fdip_cat3 WHERE reg_no = ?'
            sql_ex_str2 ='SELECT Class1 + Class2 + Class3 + Class4+ Class5 +Class6 + Class7 as TOTAL_ATT FROM Attendance_fdip_cat3 WHERE reg_no = ?'
    elif choice[0] == 'dc':
        if choice[1] == 'cat1':
            sql_ex_str = 'SELECT * FROM Attendance_dc_cat1 WHERE reg_no = ?'
            sql_ex_str2 ='SELECT Class1 + Class2 + Class3 + Class4+ Class5 +Class6 + Class7 as TOTAL_ATT FROM Attendance_dc_cat1 WHERE reg_no = ?'
        elif choice[1] == 'cat2':
            sql_ex_str = 'SELECT * FROM Attendance_dc_cat2 WHERE reg_no = ?'
            sql_ex_str2 ='SELECT Class1 + Class2 + Class3 + Class4+ Class5 +Class6 + Class7 as TOTAL_ATT FROM Attendance_dc_cat2 WHERE reg_no = ?'
        else:
            sql_ex_str = 'SELECT * FROM Attendance_dc_cat3 WHERE reg_no = ?'
            sql_ex_str2 ='SELECT Class1 + Class2 + Class3 + Class4+ Class5 +Class6 + Class7 as TOTAL_ATT FROM Attendance_dc_cat3 WHERE reg_no = ?'
    conn=sqlite3.connect(db_locale)
    c=conn.cursor()
    x=c.execute(sql_ex_str,[x2])
    names = [description[0] for description in x.description]
    student_data=c.fetchall()
    y=c.execute(sql_ex_str2,[x2])
    sum_data=c.fetchall()
    return (student_data,names,sum_data)
def att_from_db2():
    conn=sqlite3.connect(db_locale)
    c=conn.cursor()
    x=c.execute("""
    SELECT * FROM Attendance_fat_cat1
    """)
    names = [description[0] for description in x.description]
    student_data=c.fetchall()
    return (student_data,names)
@app.route("/view/<cname>", methods=['GET', 'POST'])
def view(cname):
           course1 = cname
           return render_template('batchselect.html',course1=course1)


@app.route("/view_att/<cname>", methods=['GET', 'POST'])
def view_att(cname):
    if request.method == 'POST':
        if request.form.get("submit"):
           class1 = request.form['courses']
           course1 = cname
           db_locale = "student.db"
           conn = sqlite3.connect(db_locale)
           conn.row_factory = sqlite3.Row
           c = conn.cursor()
           d = conn.cursor()
           if cname == "Principles of Operating System":
            if class1 == "C1":
                c.execute('SELECT name,course,reg_no,Class1 FROM Attendance_pos_cat1')
                d.execute('SELECT count(*) from Attendance_pos_cat1 where Class1 = "Present" ')
                data = c.fetchall()
                data1 = d.fetchall()
            if class1 == "C2":
                c.execute('SELECT name,course,reg_no,Class2 FROM Attendance_pos_cat1')
                data = c.fetchall()
                d.execute('SELECT COUNT(reg_no) FROM Attendance_pos_cat1 where CLASS2 = "Present" ')
                data1 = d.fetchall()
            if class1 == "C3":
                c.execute('SELECT name,course,reg_no,Class3 FROM Attendance_pos_cat1')
                d.execute('SELECT COUNT(reg_no) FROM Attendance_pos_cat1 where CLASS3 = "Present" ')
                data = c.fetchall()
                data1 = d.fetchall()
            if class1 == "C4":
                c.execute('SELECT name,course,reg_no,Class4 FROM Attendance_pos_cat1')
                d.execute('SELECT COUNT(reg_no) FROM Attendance_pos_cat1 where CLASS4 = "Present" ')
                data = c.fetchall()
                data1 = d.fetchall()
            if class1 == "C5":
                c.execute('SELECT name,course,reg_no,Class5 FROM Attendance_pos_cat1')
                d.execute('SELECT COUNT(reg_no) FROM Attendance_pos_cat1 where CLASS5 = "Present" ')
                data = c.fetchall()
                data1 = d.fetchall()
           if cname=="Distributed Computing":
            if class1 == "C1":
                    c.execute('SELECT name,course,reg_no,Class1 FROM Attendance_dc_cat1')
                    d.execute('SELECT COUNT(reg_no) FROM Attendance_dc_cat1 where CLASS1 = "Present" ')
                    data = c.fetchall()
                    data1 = d.fetchall()
            if class1 == "C2":
                    c.execute('SELECT name,course,reg_no,Class2 FROM Attendance_dc_cat1')
                    data = c.fetchall()
                    d.execute('SELECT COUNT(reg_no) FROM Attendance_dc_cat1 where CLASS2 = "Present" ')
                    data1 = d.fetchall()
            if class1 == "C3":
                    c.execute('SELECT name,course,reg_no,Class3 FROM Attendance_dc_cat1')
                    d.execute('SELECT COUNT(reg_no) FROM Attendance_dc_cat1 where CLASS3 = "Present" ')
                    data = c.fetchall()
                    data1 = d.fetchall()
            if class1 == "C4":
                    c.execute('SELECT name,course,reg_no,Class4 FROM Attendance_dc_cat1')
                    d.execute('SELECT COUNT(reg_no) FROM Attendance_dc_cat1 where CLASS4 = "Present" ')
                    data = c.fetchall()
                    data1 = d.fetchall()
            if class1 == "C5":
                    c.execute('SELECT name,course,reg_no,Class5 FROM Attendance_dc_cat1')
                    d.execute('SELECT COUNT(reg_no) FROM Attendance_dc_cat1 where CLASS5 = "Present" ')
                    data = c.fetchall()
                    data1 = d.fetchall()
           if cname =="Computer Network and its Applications":
            if class1 == "C1":
                    c.execute('SELECT name,course,reg_no,Class1 FROM Attendance_cna_cat1')
                    d.execute('SELECT COUNT(reg_no) FROM Attendance_cna_cat1 where CLASS1 = "Present" ')
                    data = c.fetchall()
                    data1 = d.fetchall()
            if class1 == "C2":
                    c.execute('SELECT name,course,reg_no,Class2 FROM Attendance_cna_cat1')
                    data = c.fetchall()
                    d.execute('SELECT COUNT(reg_no) FROM Attendance_cna_cat1 where CLASS2 = "Present" ')
                    data1 = d.fetchall()
            if class1 == "C3":
                    c.execute('SELECT name,course,reg_no,Class3 FROM Attendance_cna_cat1')
                    d.execute('SELECT COUNT(reg_no) FROM Attendance_cna_cat1 where CLASS3 = "Present" ')
                    data = c.fetchall()
                    data1 = d.fetchall()
            if class1 == "C4":
                    c.execute('SELECT name,course,reg_no,Class4 FROM Attendance_cna_cat1')
                    d.execute('SELECT COUNT(reg_no) FROM Attendance_cna_cat1 where CLASS4 = "Present" ')
                    data = c.fetchall()
                    data1 = d.fetchall()
            if class1 == "C5":
                    c.execute('SELECT name,course,reg_no,Class5 FROM Attendance_cna_cat1')
                    d.execute('SELECT COUNT(reg_no) FROM Attendance_cna_cat1 where CLASS5 = "Present" ')
                    data = c.fetchall()
                    data1 = d.fetchall()
           if cname == "Software Design Lab":
            if class1 == "C1":
                    c.execute('SELECT name,course,reg_no,Class1 FROM Attendance_sdlab_cat1')
                    d.execute('SELECT COUNT(reg_no) FROM Attendance_sdlab_cat1 where CLASS1 = "Present" ')
                    data = c.fetchall()
                    data1 = d.fetchall()
            if class1 == "C2":
                    c.execute('SELECT name,course,reg_no,Class2 FROM Attendance_sdlab_cat1')
                    data = c.fetchall()
                    d.execute('SELECT COUNT(reg_no) FROM Attendance_sdlab_cat1 where CLASS2 = "Present" ')
                    data1 = d.fetchall()
            if class1 == "C3":
                    c.execute('SELECT name,course,reg_no,Class3 FROM Attendance_sdlab_cat1')
                    d.execute('SELECT COUNT(reg_no) FROM Attendance_sdlab_cat1 where CLASS3 = "Present" ')
                    data = c.fetchall()
                    data1 = d.fetchall()
            if class1 == "C4":
                    c.execute('SELECT name,course,reg_no,Class4 FROM Attendance_sdlab_cat1')
                    d.execute('SELECT COUNT(reg_no) FROM Attendance_sdlab_cat1 where CLASS4 = "Present" ')
                    data = c.fetchall()
                    data1 = d.fetchall()
            if class1 == "C5":
                    c.execute('SELECT name,course,reg_no,Class5 FROM Attendance_sdlab_cat1')
                    d.execute('SELECT COUNT(reg_no) FROM Attendance_sdlab_cat1 where CLASS5 = "Present" ')
                    data = c.fetchall()
                    data1 = d.fetchall()
           if cname == "Operating Systems Lab":
            if class1 == "C1":
                   c.execute('SELECT name,course,reg_no,Class1 FROM Attendance_oslab_cat1')
                   d.execute('SELECT COUNT(reg_no) FROM Attendance_oslab_cat1 where CLASS1 = "Present" ')
                   data = c.fetchall()
                   data1 = d.fetchall()
            if class1 == "C2":
                   c.execute('SELECT name,course,reg_no,Class2 FROM Attendance_oslab_cat1')
                   data = c.fetchall()
                   d.execute('SELECT COUNT(reg_no) FROM Attendance_oslab_cat1 where CLASS2 = "Present" ')
                   data1 = d.fetchall()
            if class1 == "C3":
                   c.execute('SELECT name,course,reg_no,Class3 FROM Attendance_oslab_cat1')
                   d.execute('SELECT COUNT(reg_no) FROM Attendance_oslab_cat1 where CLASS3 = "Present" ')
                   data = c.fetchall()
                   data1 = d.fetchall()
            if class1 == "C4":
                   c.execute('SELECT name,course,reg_no,Class4 FROM Attendance_oslab_cat1')
                   d.execute('SELECT COUNT(reg_no) FROM Attendance_oslab_cat1 where CLASS4 = "Present" ')
                   data = c.fetchall()
                   data1 = d.fetchall()
            if class1 == "C5":
                   c.execute('SELECT name,course,reg_no,Class5 FROM Attendance_oslab_cat1')
                   d.execute( 'SELECT COUNT(reg_no) FROM Attendance_oslab_cat1 where CLASS5 = "Present" ')
                   data = c.fetchall()
                   data1 = d.fetchall()
        return render_template('view_att.html',course1=course1,data=data,class1=class1,data1=data1)


@app.route("/sub/<cname>", methods=['GET', 'POST'])
def edit_att(cname):
    if request.method == 'POST':
        if request.form.get("submit"):
            class1 = request.form['courses']
            type1 = request.form['student1']
            type2 = request.form['student2']
            type3 = request.form['student3']
            type4 = request.form['student4']
            type5 = request.form['student5']
            type6 = request.form['student6']
            type7 = request.form['student7']
            db_locale = "student.db"
            conn = sqlite3.connect(db_locale)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            if cname == "Principles of Operating System":
                 if class1 == "C1":
                    c.execute("Update Attendance_pos_cat1 set Class1 = ? where reg_no ='195002001'",(type1,))
                    c.execute("Update Attendance_pos_cat1 set Class1 = ? where reg_no ='195002002' ",(type2,))
                    c.execute("Update Attendance_pos_cat1 set Class1 = ? where reg_no ='195002003'",(type3,))
                    c.execute("Update Attendance_pos_cat1 set Class1 = ? where reg_no ='195002004'",(type4,))
                    c.execute("Update Attendance_pos_cat1 set Class1 = ? where reg_no ='195002005'",(type5,))
                    c.execute("Update Attendance_pos_cat1 set Class1 = ? where reg_no ='195002006'",(type6,))
                    c.execute("Update Attendance_pos_cat1 set Class1 = ? where reg_no ='195002007'",(type7,))
                    conn.commit()
                    conn.close()
                 elif class1 == "C2":
                     c.execute("Update Attendance_pos_cat1 set Class2 = ? where reg_no ='195002001'",(type1,))
                     c.execute("Update Attendance_pos_cat1 set Class2 = ? where reg_no ='195002002'",(type2,))
                     c.execute("Update Attendance_pos_cat1 set Class2 = ? where reg_no ='195002003'",(type3,))
                     c.execute("Update Attendance_pos_cat1 set Class2 = ? where reg_no ='195002004'",(type4,))
                     c.execute("Update Attendance_pos_cat1 set Class2 = ? where reg_no ='195002005'",(type5,))
                     c.execute("Update Attendance_pos_cat1 set Class2 = ? where reg_no ='195002006'",(type6,))
                     c.execute("Update Attendance_pos_cat1 set Class2 = ? where reg_no ='195002007'",(type7,))
                     conn.commit()
                     conn.close()
                 elif class1 == "C3":
                     c.execute("Update Attendance_pos_cat1 set Class3 = ? where reg_no ='195002001'",(type1,))
                     c.execute("Update Attendance_pos_cat1 set Class3 = ? where reg_no ='195002002'", (type2,))
                     c.execute("Update Attendance_pos_cat1 set Class3 = ? where reg_no ='195002003'", (type3,))
                     c.execute("Update Attendance_pos_cat1 set Class3 = ? where reg_no ='195002004'", (type4,))
                     c.execute("Update Attendance_pos_cat1 set Class3 = ? where reg_no ='195002005'", (type5,))
                     c.execute("Update Attendance_pos_cat1 set Class3 = ? where reg_no ='195002006'",(type6,))
                     c.execute("Update Attendance_pos_cat1 set Class3 = ? where reg_no ='195002007'",(type7,))
                     conn.commit()
                     conn.close()
                 elif class1 == "C4":
                     c.execute("Update Attendance_pos_cat1 set Class4 = ? where reg_no ='195002001'",(type1,))
                     c.execute("Update Attendance_pos_cat1 set Class4 = ? where reg_no ='195002002'",(type2,))
                     c.execute("Update Attendance_pos_cat1 set Class4 = ? where reg_no ='195002003'",(type3,))
                     c.execute("Update Attendance_pos_cat1 set Class4 = ? where reg_no ='195002004'",(type4,))
                     c.execute("Update Attendance_pos_cat1 set Class4 = ? where reg_no ='195002005' ",(type5,))
                     c.execute("Update Attendance_pos_cat1 set Class4 = ? where reg_no ='195002006'",(type6,))
                     c.execute("Update Attendance_pos_cat1 set Class4 = ? where reg_no ='195002007'",(type7,))
                     conn.commit()
                     conn.close()
                 elif class1 == "C15":
                     c.execute("Update Attendance_pos_cat1 set Class5 = ? where reg_no ='195002001'",(type1,))
                     c.execute("Update Attendance_pos_cat1 set Class5 = ? where reg_no ='195002002'",(type2,))
                     c.execute("Update Attendance_pos_cat1 set Class5 = ? where reg_no ='195002003'",(type3,))
                     c.execute("Update Attendance_pos_cat1 set Class5 = ? where reg_no ='195002004'",(type4,))
                     c.execute("Update Attendance_pos_cat1 set Class5 = ? where reg_no ='195002005'",(type5,))
                     c.execute("Update Attendance_pos_cat1 set Class5 = ? where reg_no ='195002006'",(type6,))
                     c.execute("Update Attendance_pos_cat1 set Class5 = ? where reg_no ='195002007'" ,(type7,)) 
                     conn.commit()
                     conn.close()
            if cname == "Distributed Computing":
                 if class1 == "C1":
                    c.execute("Update Attendance_dc_cat1 set Class1 = ? where reg_no ='195002001' ", (type1,))
                    c.execute("Update Attendance_dc_cat1 set Class1 = ? where reg_no ='195002002' ", (type2,))
                    c.execute("Update Attendance_dc_cat1 set Class1 = ? where reg_no ='195002003'", (type3,))
                    c.execute("Update Attendance_dc_cat1 set Class1 = ? where reg_no ='195002004'", (type4,))
                    c.execute("Update Attendance_dc_cat1 set Class1 = ? where reg_no ='195002005'", (type5,))
                    c.execute("Update Attendance_dc_cat1 set Class1 = ? where reg_no ='195002006'", (type6,))
                    c.execute("Update Attendance_dc_cat1 set Class1 = ? where reg_no ='195002007'", (type7,))
                    conn.commit()
                    conn.close()
                 elif class1 == "C2":
                    c.execute("Update Attendance_dc_cat1 set Class2 = ? where reg_no ='195002001'", (type1,))
                    c.execute("Update Attendance_dc_cat1 set Class2 = ? where reg_no ='195002002'", (type2,))
                    c.execute("Update Attendance_dc_cat1 set Class2 = ? where reg_no ='195002003' ", (type3,))
                    c.execute("Update Attendance_dc_cat1 set Class2 = ? where reg_no ='195002004' ", (type4,))
                    c.execute("Update Attendance_dc_cat1 set Class2 = ? where reg_no ='195002005' ", (type5,))
                    c.execute("Update Attendance_dc_cat1 set Class2 = ? where reg_no ='195002006' ", (type6,))
                    c.execute("Update Attendance_dc_cat1 set Class2 = ? where reg_no ='195002007'", (type7,))
                    conn.commit()
                    conn.close()
                 elif class1 == "C3":
                    c.execute("Update Attendance_dc_cat1 set Class3 = ? where reg_no ='195002001'", (type1,))
                    c.execute("Update Attendance_dc_cat1 set Class3 = ? where reg_no ='195002002'", (type2,))
                    c.execute("Update Attendance_dc_cat1 set Class3 = ? where reg_no ='195002003'", (type3,))
                    c.execute("Update Attendance_dc_cat1 set Class3 = ? where reg_no ='195002004'", (type4,))
                    c.execute("Update Attendance_dc_cat1 set Class3 = ? where reg_no ='195002005'", (type5,))
                    c.execute("Update Attendance_dc_cat1 set Class3 = ? where reg_no ='195002006'", (type6,))
                    c.execute("Update Attendance_dc_cat1 set Class3 = ? where reg_no ='195002007'", (type7,))
                    conn.commit()
                    conn.close()
                 elif class1 == "C4":
                    c.execute("Update Attendance_dc_cat1 set Class4 = ? where reg_no ='195002001'", (type1,))
                    c.execute("Update Attendance_dc_cat1 set Class4 = ? where reg_no ='195002002'", (type2,))
                    c.execute("Update Attendance_dc_cat1 set Class4 = ? where reg_no ='195002003'", (type3,))
                    c.execute("Update Attendance_dc_cat1 set Class4 = ? where reg_no ='195002004'", (type4,))
                    c.execute("Update Attendance_dc_cat1 set Class4 = ? where reg_no ='195002005' ", (type5,))
                    c.execute("Update Attendance_dc_cat1 set Class4 = ? where reg_no ='195002006'", (type6,))
                    c.execute("Update Attendance_dc_cat1 set Class4 = ? where reg_no ='195002007' ", (type7,))
                    conn.commit()
                    conn.close()
                 else:
                    c.execute("Update Attendance_dc_cat1 set Class5 = ? where reg_no ='195002001'", (type1,))
                    c.execute("Update Attendance_dc_cat1 set Class5 = ? where reg_no ='195002002'", (type2,))
                    c.execute("Update Attendance_dc_cat1 set Class5 = ? where reg_no ='195002003'", (type3,))
                    c.execute("Update Attendance_dc_cat1 set Class5 = ? where reg_no ='195002004' ", (type4,))
                    c.execute("Update Attendance_dc_cat1 set Class5 = ? where reg_no ='195002005' ", (type5,))
                    c.execute("Update Attendance_dc_cat1 set Class5 = ? where reg_no ='195002006' ", (type6,))
                    c.execute("Update Attendance_dc_cat1 set Class5 = ? where reg_no ='195002007'", (type7,))
                    conn.commit()
                    conn.close()
        if cname == "Computer Network and its Applications":
            if class1 == "C1":
             c.execute("Update Attendance_cna_cat1 set Class1 = ? where reg_no ='195002001' ", (type1,))
             c.execute("Update Attendance_cna_cat1 set Class1 = ? where reg_no ='195002002' ", (type2,))
             c.execute("Update Attendance_cna_cat1 set Class1 = ? where reg_no ='195002003'", (type3,))
             c.execute("Update Attendance_cna_cat1 set Class1 = ? where reg_no ='195002004'", (type4,))
             c.execute("Update Attendance_cna_cat1 set Class1 = ? where reg_no ='195002005'", (type5,))
             c.execute("Update Attendance_cna_cat1 set Class1 = ? where reg_no ='195002006'", (type6,))
             c.execute("Update Attendance_cna_cat1 set Class1 = ? where reg_no ='195002007'", (type7,))
             conn.commit()
             conn.close()
            elif class1 == "C2":
             c.execute("Update Attendance_cna_cat1 set Class2 = ? where reg_no ='195002001'", (type1,))
             c.execute("Update Attendance_cna_cat1 set Class2 = ? where reg_no ='195002002'", (type2,))
             c.execute("Update Attendance_cna_cat1 set Class2 = ? where reg_no ='195002003' ", (type3,))
             c.execute("Update Attendance_cna_cat1 set Class2 = ? where reg_no ='195002004' ", (type4,))
             c.execute("Update Attendance_cna_cat1 set Class2 = ? where reg_no ='195002005' ", (type5,))
             c.execute("Update Attendance_cna_cat1 set Class2 = ? where reg_no ='195002006' ", (type6,))
             c.execute("Update Attendance_cna_cat1 set Class2 = ? where reg_no ='195002007'", (type7,))
             conn.commit()
             conn.close()
            elif class1 == "C3":
             c.execute("Update Attendance_cna_cat1 set Class3 = ? where reg_no ='195002001'", (type1,))
             c.execute("Update Attendance_cna_cat1 set Class3 = ? where reg_no ='195002002'", (type2,))
             c.execute("Update Attendance_cna_cat1 set Class3 = ? where reg_no ='195002003'", (type3,))
             c.execute("Update Attendance_cna_cat1 set Class3 = ? where reg_no ='195002004'", (type4,))
             c.execute("Update Attendance_cna_cat1 set Class3 = ? where reg_no ='195002005'", (type5,))
             c.execute("Update Attendance_cna_cat1 set Class3 = ? where reg_no ='195002006'", (type6,))
             c.execute("Update Attendance_cna_cat1 set Class3 = ? where reg_no ='195002007'", (type7,))
             conn.commit()
             conn.close()
            elif class1 == "C4":
             c.execute("Update Attendance_cna_cat1 set Class4 = ? where reg_no ='195002001'", (type1,))
             c.execute("Update Attendance_cna_cat1 set Class4 = ? where reg_no ='195002002'", (type2,))
             c.execute("Update Attendance_cna_cat1 set Class4 = ? where reg_no ='195002003'", (type3,))
             c.execute("Update Attendance_cna_cat1 set Class4 = ? where reg_no ='195002004'", (type4,))
             c.execute("Update Attendance_cna_cat1 set Class4 = ? where reg_no ='195002005' ", (type5,))
             c.execute("Update Attendance_cna_cat1 set Class4 = ? where reg_no ='195002006'", (type6,))
             c.execute("Update Attendance_cna_cat1 set Class4 = ? where reg_no ='195002007' ", (type7,))
             conn.commit()
             conn.close()
            else:
             c.execute("Update Attendance_cna_cat1 set Class5 = ? where reg_no ='195002001'", (type1,))
             c.execute("Update Attendance_cna_cat1 set Class5 = ? where reg_no ='195002002'", (type2,))
             c.execute("Update Attendance_cna_cat1 set Class5 = ? where reg_no ='195002003'", (type3,))
             c.execute("Update Attendance_cna_cat1 set Class5 = ? where reg_no ='195002004' ", (type4,))
             c.execute("Update Attendance_cna_cat1 set Class5 = ? where reg_no ='195002005' ", (type5,))
             c.execute("Update Attendance_cna_cat1 set Class5 = ? where reg_no ='195002006' ", (type6,))
             c.execute("Update Attendance_cna_cat1 set Class5 = ? where reg_no ='195002007'", (type7,))
             conn.commit()
             conn.close()   
        if cname == "Software Design Lab":
         if class1 == "C1":
             c.execute("Update Attendance_sdlab_cat1 set Class1 = ? where reg_no ='195002001' ", (type1,))
             c.execute("Update Attendance_sdlab_cat1 set Class1 = ? where reg_no ='195002002' ", (type2,))
             c.execute("Update Attendance_sdlab_cat1 set Class1 = ? where reg_no ='195002003'", (type3,))
             c.execute("Update Attendance_sdlab_cat1 set Class1 = ? where reg_no ='195002004'", (type4,))
             c.execute("Update Attendance_sdlab_cat1 set Class1 = ? where reg_no ='195002005'", (type5,))
             c.execute("Update Attendance_sdlab_cat1 set Class1 = ? where reg_no ='195002006'", (type6,))
             c.execute("Update Attendance_sdlab_cat1 set Class1 = ? where reg_no ='195002007'", (type7,))
             conn.commit()
             conn.close()
         elif class1 == "C2":
             c.execute("Update Attendance_sdlab_cat1 set Class2 = ? where reg_no ='195002001'", (type1,))
             c.execute("Update Attendance_sdlab_cat1 set Class2 = ? where reg_no ='195002002'", (type2,))
             c.execute("Update Attendance_sdlab_cat1 set Class2 = ? where reg_no ='195002003' ", (type3,))
             c.execute("Update Attendance_sdlab_cat1 set Class2 = ? where reg_no ='195002004' ", (type4,))
             c.execute("Update Attendance_sdlab_cat1 set Class2 = ? where reg_no ='195002005' ", (type5,))
             c.execute("Update Attendance_sdlab_cat1 set Class2 = ? where reg_no ='195002006' ", (type6,))
             c.execute("Update Attendance_sdlab_cat1 set Class2 = ? where reg_no ='195002007'", (type7,))
             conn.commit()
             conn.close()
         elif class1 == "C3":
             c.execute("Update Attendance_sdlab_cat1 set Class3 = ? where reg_no ='195002001'", (type1,))
             c.execute("Update Attendance_sdlab_cat1 set Class3 = ? where reg_no ='195002002'", (type2,))
             c.execute("Update Attendance_sdlab_cat1 set Class3 = ? where reg_no ='195002003'", (type3,))
             c.execute("Update Attendance_sdlab_cat1 set Class3 = ? where reg_no ='195002004'", (type4,))
             c.execute("Update Attendance_sdlab_cat1 set Class3 = ? where reg_no ='195002005'", (type5,))
             c.execute("Update Attendance_sdlab_cat1 set Class3 = ? where reg_no ='195002006'", (type6,))
             c.execute("Update Attendance_sdlab_cat1 set Class3 = ? where reg_no ='195002007'", (type7,))
             conn.commit()
             conn.close()
         elif class1 == "C4":
             c.execute("Update Attendance_sdlab_cat1 set Class4 = ? where reg_no ='195002001'", (type1,))
             c.execute("Update Attendance_sdlab_cat1 set Class4 = ? where reg_no ='195002002'", (type2,))
             c.execute("Update Attendance_sdlab_cat1 set Class4 = ? where reg_no ='195002003'", (type3,))
             c.execute("Update Attendance_sdlab_cat1 set Class4 = ? where reg_no ='195002004'", (type4,))
             c.execute("Update Attendance_sdlab_cat1 set Class4 = ? where reg_no ='195002005' ", (type5,))
             c.execute("Update Attendance_sdlab_cat1 set Class4 = ? where reg_no ='195002006'", (type6,))
             c.execute("Update Attendance_sdlab_cat1 set Class4 = ? where reg_no ='195002007' ", (type7,))
             conn.commit()
             conn.close()
         else:
             c.execute("Update Attendance_sdlab_cat1 set Class5 = ? where reg_no ='195002001'", (type1,))
             c.execute("Update Attendance_sdlab_cat1 set Class5 = ? where reg_no ='195002002'", (type2,))
             c.execute("Update Attendance_sdlab_cat1 set Class5 = ? where reg_no ='195002003'", (type3,))
             c.execute("Update Attendance_sdlab_cat1 set Class5 = ? where reg_no ='195002004' ", (type4,))
             c.execute("Update Attendance_sdlab_cat1 set Class5 = ? where reg_no ='195002005' ", (type5,))
             c.execute("Update Attendance_sdlab_cat1 set Class5 = ? where reg_no ='195002006' ", (type6,))
             c.execute("Update Attendance_sdlab_cat1 set Class5 = ? where reg_no ='195002007'", (type7,))
             conn.commit()
             conn.close()       
        if cname == "Operating Systems Lab":
         if class1 == "C1":
             c.execute("Update Attendance_oslab_cat1 set Class1 = ? where reg_no ='195002001' ", (type1,))
             c.execute("Update Attendance_oslab_cat1 set Class1 = ? where reg_no ='195002002' ", (type2,))
             c.execute("Update Attendance_oslab_cat1 set Class1 = ? where reg_no ='195002003'", (type3,))
             c.execute("Update Attendance_oslab_cat1 set Class1 = ? where reg_no ='195002004'", (type4,))
             c.execute("Update Attendance_oslab_cat1 set Class1 = ? where reg_no ='195002005'", (type5,))
             c.execute("Update Attendance_oslab_cat1 set Class1 = ? where reg_no ='195002006'", (type6,))
             c.execute("Update Attendance_oslab_cat1 set Class1 = ? where reg_no ='195002007'", (type7,))
             conn.commit()
             conn.close()
         elif class1 == "C2":
             c.execute("Update Attendance_oslab_cat1 set Class2 = ? where reg_no ='195002001'", (type1,))
             c.execute("Update Attendance_oslab_cat1 set Class2 = ? where reg_no ='195002002'", (type2,))
             c.execute("Update Attendance_oslab_cat1 set Class2 = ? where reg_no ='195002003' ", (type3,))
             c.execute("Update Attendance_oslab_cat1 set Class2 = ? where reg_no ='195002004' ", (type4,))
             c.execute("Update Attendance_oslab_cat1 set Class2 = ? where reg_no ='195002005' ", (type5,))
             c.execute("Update Attendance_oslab_cat1 set Class2 = ? where reg_no ='195002006' ", (type6,))
             c.execute("Update Attendance_oslab_cat1 set Class2 = ? where reg_no ='195002007'", (type7,))
             conn.commit()
             conn.close()
         elif class1 == "C3":
             c.execute("Update Attendance_oslab_cat1 set Class3 = ? where reg_no ='195002001'", (type1,))
             c.execute("Update Attendance_oslab_cat1 set Class3 = ? where reg_no ='195002002'", (type2,))
             c.execute("Update Attendance_oslab_cat1 set Class3 = ? where reg_no ='195002003'", (type3,))
             c.execute("Update Attendance_oslab_cat1 set Class3 = ? where reg_no ='195002004'", (type4,))
             c.execute("Update Attendance_oslab_cat1 set Class3 = ? where reg_no ='195002005'", (type5,))
             c.execute("Update Attendance_oslab_cat1 set Class3 = ? where reg_no ='195002006'", (type6,))
             c.execute("Update Attendance_oslab_cat1 set Class3 = ? where reg_no ='195002007'", (type7,))
             conn.commit()
             conn.close()
         elif class1 == "C4":
             c.execute("Update Attendance_oslab_cat1 set Class4 = ? where reg_no ='195002001'", (type1,))
             c.execute("Update Attendance_oslab_cat1 set Class4 = ? where reg_no ='195002002'", (type2,))
             c.execute("Update Attendance_oslab_cat1 set Class4 = ? where reg_no ='195002003'", (type3,))
             c.execute("Update Attendance_oslab_cat1 set Class4 = ? where reg_no ='195002004'", (type4,))
             c.execute("Update Attendance_oslab_cat1 set Class4 = ? where reg_no ='195002005' ", (type5,))
             c.execute("Update Attendance_oslab_cat1 set Class4 = ? where reg_no ='195002006'", (type6,))
             c.execute("Update Attendance_oslab_cat1 set Class4 = ? where reg_no ='195002007' ", (type7,))
             conn.commit()
             conn.close()
         else:
             c.execute("Update Attendance_oslab_cat1 set Class5 = ? where reg_no ='195002001'", (type1,))
             c.execute("Update Attendance_oslab_cat1 set Class5 = ? where reg_no ='195002002'", (type2,))
             c.execute("Update Attendance_oslab_cat1 set Class5 = ? where reg_no ='195002003'", (type3,))
             c.execute("Update Attendance_oslab_cat1 set Class5 = ? where reg_no ='195002004' ", (type4,))
             c.execute("Update Attendance_oslab_cat1 set Class5 = ? where reg_no ='195002005' ", (type5,))
             c.execute("Update Attendance_oslab_cat1 set Class5 = ? where reg_no ='195002006' ", (type6,))
             c.execute("Update Attendance_oslab_cat1 set Class5 = ? where reg_no ='195002007'", (type7,))
             conn.commit()
             conn.close()   
        return render_template('edit_att.html')
@app.route("/batch")

def batch():
	return render_template("batchselectm.html")


@app.route("/sub",methods=['POST'])
def sub():
	
	cname=request.form["coursename"]
	dur=request.form["dur"]
	print(dur)
	con=sqlite3.connect("student.db")
	con.row_factory=sqlite3.Row
	cur=con.cursor()
	if dur=="cat1":
		cur.execute('SELECT reg_no,present FROM Attendance_fat_cat1 ')
		data=cur.fetchall()
	if dur=="cat2":
		cur.execute('SELECT reg_no,present  FROM Attendance_fat_cat2')
		data=cur.fetchall()
	if dur=="cat2":
		cur.execute('SELECT reg_no,present  FROM Attendance_fat_cat2')
		data=cur.fetchall()
	
	
	
	con.close()
	return render_template("coursewise.html",data=data,dur=dur,cname=cname)

@app.route("/catwise")

def catwise():
	return render_template("catselect.html")

@app.route("/viewm",methods=['POST'])
def view2():

	
	catname=request.form["period"]
	sem=request.form["semester"]
	print(sem)
	con=sqlite3.connect("student.db")
	con.row_factory=sqlite3.Row
	cur=con.cursor()
	print(catname)
	if catname=="cat1":
		cur.execute('SELECT * FROM Attendance_fat_cat1')
		data=cur.fetchall()
	if catname=="cat2":
		cur.execute('SELECT * FROM Attendance_fat_cat2')
		data=cur.fetchall()
	if catname=="cat2":
		cur.execute('SELECT * FROM Attendance_fat_cat2')
		data=cur.fetchall()
	
	
	
	con.close()
	return render_template("catwise.html",data=data,sem=sem,catname=catname)




@app.route("/hod")
def hod():
	return render_template("hod.html")

@app.route("/batch_hod")

def batch_hod():
	return render_template("batchselect_hod.html")

@app.route("/ins",methods=['POST'])
def ins():
	curname=request.form["coursename"]
	duration=request.form["dur"]
	print(duration)
	con=sqlite3.connect("student.db")
	con.row_factory=sqlite3.Row
	cur=con.cursor()
	
	if duration=="cat1":
		cur.execute('SELECT * FROM Attendance_fat_cat1')
		data=cur.fetchall()
	if duration=="cat2":
		cur.execute('SELECT * FROM Attendance_fat_cat2')
		data=cur.fetchall()
	if duration=="cat2":
		cur.execute('SELECT * FROM Attendance_fat_cat2')
		data=cur.fetchall()
	
	
	
	con.close()
	return render_template("coursewise_hod.html",data=data,duration=duration,curname=curname)



@app.route("/catwise_hod")

def catwise_hod():
	return render_template("catselect_hod.html")

@app.route("/view_hod",methods=['POST'])
def view_hod():

	catname=request.form["period"]
	sem=request.form["semester"]
	print(sem)
	con=sqlite3.connect("student.db")
	con.row_factory=sqlite3.Row
	cur=con.cursor()
	print(catname)
	if catname=="cat1":
		cur.execute('SELECT * FROM Attendance_fat_cat1')
		data=cur.fetchall()
	if catname=="cat2":
		cur.execute('SELECT * FROM Attendance_fat_cat2')
		data=cur.fetchall()
	if catname=="cat3":
		cur.execute('SELECT * FROM Attendance_fat_cat3')
		data=cur.fetchall()
	con.close()
	return render_template("catwise_hod.html",data=data,sem=sem,catname=catname)

if __name__=='__main__':
    app.run()