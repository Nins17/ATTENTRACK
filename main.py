from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from admin import admin,mysql
import os
import csv
import numpy as np
from datetime import datetime
import cv2
import face_recognition


app = Flask(__name__)
app.register_blueprint(admin, url_prefix="/admin")
app.secret_key = "ams"

# MySQL Config
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Rootpassword@l03e1t3'
app.config['MYSQL_DATABASE_DB'] = 'ams'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# Initialize MySQL
mysql.init_app(app)

SAVE_DIR = 'static/known_faces'
os.makedirs(SAVE_DIR, exist_ok=True)

#for csv file 
datetoday = datetime.now().strftime("%m_%d_%y") 
yeartoday = datetime.now().year
current_schoolyear = yeartoday-1 
CSV_DIR = 'static/attendance_csv'
os.makedirs(CSV_DIR, exist_ok=True)

       
#global functions
def get_db_cursor():
    conn = mysql.connect()
    cursor = conn.cursor()
    return cursor, conn
def false_login():
    flash("Please Login first",'error')
    return redirect(url_for('login_teacher_form'))


#routes
#landing
@app.route('/')
def index():
    return render_template("index.html")


########## TEACHER SIDE ########## 

@app.route('/login_teacher_form', methods=["POST", "GET"])
def login_teacher_form():
    return render_template("user/forms/login_teacher.html")

@app.route('/user_home', methods=["POST", "GET"])
def user_home():
    if session.get('teacher_logged_in')==True:
        teacherinfo= session.get('logged_teacher')
        cursor, conn = get_db_cursor()
        cursor.execute('SELECT * FROM class_schedules WHERE teacher_id=%s',(session.get('teacher_id')))
        class_scheds=cursor.fetchall()
        print(f"####{teacherinfo}")
        return render_template("user/teacher_index.html",logged_teacher=teacherinfo, class_scheds=class_scheds)
    else:
        return false_login()
    
@app.route('/login_teacher', methods=["POST","GET"])
def login_teacher():
    if request.method == "POST":
        teacher_id = int(request.form["teacher_id"])
        teacher_pass = str(request.form["teacher_pass"])
    
        
        cursor, conn = get_db_cursor()
        cursor.execute(
            "SELECT * FROM teacher_accounts WHERE teacher_ID=%s AND teacher_password=%s",
            (teacher_id, teacher_pass)
        )
        teacher = cursor.fetchone()
        print(teacher)

        if not teacher:
            flash('No Account Found', 'error')
            return redirect(url_for('login_teacher_form'))

        # If password is default (same as teacher ID), redirect to update password
        if teacher[6] == f"{teacher_id}":
            session["temp_teacher_id"] = teacher[0]
            session["temp"]= True
            return redirect(url_for('update_teacher_password_form'))

        # Set session for logged-in teacher
        session["teacher_logged_in"] = True
        session["teacher_id"] = teacher[0]
        session["teacher_pass"] = teacher[6]
        session["teacher_name"] = teacher[2]
        session["logged_teacher"] = teacher  # full DB row
        return redirect('user_home')

    else:
        return false_login()

@app.route('/update_teacher_password_form')
def update_teacher_password_form():
    if session.get('temp')==True:
        session['teacher_id'] = session.get('temp_teacher_id')
        return render_template("user/forms/update_teacher_password_form.html")   
    else:
        return false_login()

@app.route("/update_teacher_password", methods=['POST'])
def update_teacher_password():
    if request.method == "POST":
        teacher_id = session.get('teacher_id')
        new_pass = request.form["teacher_id"]
        pass_confirm = request.form["teacher_pass"]
            
        cursor, conn = get_db_cursor()

        if new_pass == pass_confirm:    
                # Check for at least one uppercase letter
            has_upper = any(c.isupper() for c in new_pass)
                # Check for at least one symbol
            symbols = "!@#$%^&*(),.?\":{}|<>"
            has_symbol = any(c in symbols for c in new_pass)
            valid_passlen= len(new_pass)>=8
            if not has_upper or not has_symbol: 
                flash("Password must contain at least one uppercase letter  at least one symbol", 'error')
                return redirect(url_for('update_teacher_password_form', teacher_id=teacher_id))
            if not valid_passlen:
                flash("Password too short", 'error')
                return redirect(url_for('update_teacher_password_form', teacher_id=teacher_id))
            else:
                cursor.execute("UPDATE `ams`.`teacher_accounts` SET `teacher_password` = %s WHERE (`teacher_ID` = %s);", (new_pass,teacher_id))
                conn.commit()
                cursor.close()
                flash("Successfully Updated Password, Login to continue",'success')
                return redirect(url_for('login_teacher_form'))
        else:
            flash("Password didn't match",'error')
            return redirect(url_for('update_teacher_password_form'))   

@app.route('/view_student_list')
def view_student_list():
    if session.get('teacher_logged_in')==True:
        teacher_id=int(session.get('teacher_id'))
        cursor, conn = get_db_cursor()  
    
        query = """
        SELECT DISTINCT student_id
        FROM student_schedule_enrollments
        WHERE teacher_id = %s
    """
    cursor.execute(query, (teacher_id,))
    student_ids = cursor.fetchall()  

    student_details = []
    for student in student_ids:
        student_id = student[0]
        cursor.execute("SELECT * FROM student_info WHERE student_id = %s", (student_id,))
        info = cursor.fetchone()  # fetchone because student_id is unique
        if info:
            student_details.append(info)
        
        #for table
        cursor.close() 
      
        return render_template("user/student_list.html", student_lists=student_details,logged_teacher=session.get('logged_teacher'))
    else:
        return false_login()
 
@app.route('/attendance_record', methods=["POST", "GET"])
def attendance_record():
    if session.get('teacher_logged_in')==True:
        logged_teacher= session.get('logged_teacher')
        cursor, conn = get_db_cursor()
        cursor.execute('SELECT * FROM `attendance_logs` WHERE teacher_id=%s',(session.get('teacher_id')))
        csv_files=cursor.fetchall()
        return render_template("user/attendance_record.html",logged_teacher=logged_teacher, csv_files=csv_files)
    else:
        return false_login()
 
@app.route('/class_schedules',methods=["POST", "GET"])
def class_schedules():
    if session.get('teacher_logged_in')==True:
        logged_teacher= session.get('logged_teacher')
        cursor, conn = get_db_cursor()
        cursor.execute('SELECT * FROM class_schedules WHERE teacher_id=%s',(session.get('teacher_id')))
        class_scheds=cursor.fetchall()
        teacher_name=session.get('teacher_name')
        
        
        return render_template("user/class_schedules.html",class_scheds=class_scheds,teacher_name=teacher_name, logged_teacher= logged_teacher)
    else:
        return false_login()

@app.route('/view_students_by_schedule/<int:schedule_id>')
def view_students_by_schedule(schedule_id):
    if session.get('teacher_logged_in')==True:
        teacher_id=int(session.get('teacher_id'))
        cursor, conn = get_db_cursor()
        #for checkboxes
        query = """
            SELECT *
            FROM student_schedule_enrollments
            WHERE schedule_id=%s
        """
        cursor.execute(query, (schedule_id,))
        student_lists = cursor.fetchall()
        
        #for table
        cursor.execute("SELECT * FROM class_schedules WHERE schedule_id=%s", (schedule_id,))
        fetched_sched = cursor.fetchone()
        cursor.close() 
     
        return render_template("user/students_by_schedule.html", student_lists=student_lists, sched_info=fetched_sched)
    else:
        return false_login()
    

@app.route("/take_attendance/<int:schedule_id>/<schedule_name>", methods=["POST", "GET"])
def take_attendance(schedule_id,schedule_name):
    cursor, conn = get_db_cursor()
    known_faces_dir = str(SAVE_DIR)
    known_face_encodings = []
    known_face_names = []
    teacher_id = int(session.get('teacher_id'))
    
    #for csv file 
    csvpath = f'{CSV_DIR}/{schedule_name}_{datetoday}_Attendance.csv'
    csv_name= f'{schedule_name}_{datetoday}_Attendance.csv'
    if not os.path.exists(csvpath):
        with open(csvpath, 'w') as f:
            f.write("student_id,student_name,time_in\n")
            cursor.execute("""
                    INSERT INTO `attendance_logs`(`schedule_id`,`filename`, `csv_path`, `teacher_id`) VALUES (%s,%s,%s,%s)
                """, (schedule_id,csv_name,csvpath,teacher_id ))
            conn.commit()
    # Load known faces
    for filename in os.listdir(known_faces_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            path = os.path.join(known_faces_dir, filename)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(os.path.splitext(filename)[0])


    video_capture = cv2.VideoCapture(0)
    video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
  
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 2)

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect faces and encodings
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            color = (0, 0, 255) # red

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                color = (0, 255, 0)  # green
                            
                already_logged = False
                if os.path.exists(csvpath):
                    with open(csvpath, 'r', newline='') as f:
                        reader = csv.reader(f)
                        next(reader, None)  # skip header
                        for row in reader:
                            if str(name) == row[0]:  # read student_id in column 0
                                already_logged = True
                                color = (0, 0, 255)  # RED
                                break

                if not already_logged:
                    student_id = int(name)
                    cursor.execute(
                        'SELECT * FROM `student_info` WHERE student_id = %s AND teacher_id = %s',
                        (student_id, teacher_id)
                    )
                    student_info = cursor.fetchone()

                    if student_info:
                        student_name = f"{student_info[2]} {student_info[3]} {student_info[4]}"
                        time_in = datetime.now().strftime("%H:%M:%S")

                        with open(csvpath, 'a', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow([student_id, student_name, time_in])
                            
            # Scale back up face locations
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            # Label below face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

        # Show the video
        cv2.imshow("Taking Attendance (press 'q' to close camera)", frame)

        # Quit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

      
    video_capture.release()
    cv2.destroyAllWindows()
    return redirect(url_for('user_home'))



@app.route("/search_students")
def search_students():
    query = request.args.get("query", "")
    teacher_id = session.get('teacher_id')

    cursor, conn = get_db_cursor()

    
    sql_students = """
        SELECT student_id, student_first_name, student_middle_name, student_last_name
        FROM student_info
        WHERE teacher_id = %s AND student_id LIKE %s
        ORDER BY student_last_name
    """
    cursor.execute(sql_students, (teacher_id, f"%{query}%"))
    students = cursor.fetchall()

   
    sql_scheds = """
        SELECT * 
        FROM class_schedules
        WHERE teacher_id = %s
        ORDER BY start_time
    """
    cursor.execute(sql_scheds, (teacher_id,))
    scheds = cursor.fetchall()

    cursor.close()

  
    data = {
        "students": [
            {
                "student_id": s[0],
                "first_name": s[1],
                "middle_name": s[2],
                "last_name": s[3]
            }
            for s in students
        ],
        "schedules": scheds  # list of lists, same as before
    }

    return jsonify(data)
 

    
@app.route('/sign_out')
def sign_out():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))

@app.route('/sign_out_admin')
def sign_out_admin():
    session.clear()
    flash('Admin logged out', 'success')
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)
    