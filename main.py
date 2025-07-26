from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flaskext.mysql import MySQL
import os
import numpy as np
from datetime import datetime, date
import cv2
import face_recognition


app = Flask(__name__)
app.secret_key = "ams"

# MySQL Config
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'ams'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# Initialize MySQL
mysql = MySQL()
mysql.init_app(app)

SAVE_DIR = 'static/known_faces'
os.makedirs(SAVE_DIR, exist_ok=True)

#global functions
def get_db_cursor():
    conn = mysql.connect()
    cursor = conn.cursor()
    return cursor, conn
def not_logged():
    flash('You are not logged in, Session failed!', 'error')
    return redirect(url_for('index'))

datetoday = date.today().strftime("%m_%d_%y")
datetoday2 = date.today().strftime("%d-%B-%Y")

#routes
#landing
@app.route('/')
def index():
    return render_template("index.html")

#teacher
#<----pages---->
@app.route('/login_teacher_form', methods=["POST", "GET"])
def login_teacher_form():
    return render_template("user/login_teacher.html")

@app.route('/user_home', methods=["POST", "GET"])
def user_home():
    if session.get('logged_in')==True:
        logged_teacher= session.get('logged_teacher')
        return render_template("user/index.html",logged_teacher=logged_teacher)
    else:
        return not_logged()
 

@app.route('/enrollStudentform',methods=["POST", "GET"])
def enrollStudentform():
    if session.get('logged_in')==True:
        logged_teacher= session.get('logged_teacher')
        cursor, conn = get_db_cursor()
        cursor.execute('SELECT DISTINCT grade_level FROM class_schedules WHERE teacher_id=%s',(session.get('teacher_id')))
        avail_grade_level = [row[0] for row in cursor.fetchall()]
        print(avail_grade_level)

        cursor.execute('SELECT DISTINCT section FROM class_schedules WHERE teacher_id=%s',(session.get('teacher_id')))
        avail_section = [row[0] for row in cursor.fetchall()]
        print(avail_section)
        cursor.execute('SELECT DISTINCT subject FROM class_schedules WHERE teacher_id=%s',(session.get('teacher_id')))
        avail_subject = [row[0] for row in cursor.fetchall()]
        print(avail_subject)
        
        if avail_grade_level or avail_section or avail_subject :
            return render_template("user/forms/enroll_student_form.html",avail_grade_level=avail_grade_level,avail_section=avail_section,avail_subject=avail_subject,logged_teacher=logged_teacher)
        else:
            pass
    else:
        return not_logged()
 
    
   
@app.route('/class_schedules',methods=["POST", "GET"])
def class_schedules():
    if session.get('logged_in')==True:
        logged_teacher= session.get('logged_teacher')
        cursor, conn = get_db_cursor()
        cursor.execute('SELECT * FROM class_schedules WHERE teacher_id=%s',(session.get('teacher_id')))
        class_scheds=cursor.fetchall()
        teacher_name=session.get('teacher_name')
        
        return render_template("user/class_schedules.html",class_scheds=class_scheds,teacher_name=teacher_name, logged_teacher= logged_teacher)
    else:
        return not_logged()

@app.route('/view_students_by_schedule/<int:schedule_id>')
def view_students_by_schedule(schedule_id):
    if session.get('logged_in')==True:
        teacher_id=int(session.get('teacher_id'))
        cursor, conn = get_db_cursor()
        #for checkboxes
        query = """
            SELECT student_id, student_first_name, student_middle_name, student_last_name
            FROM student_info
            WHERE teacher_id = %s
            AND student_id NOT IN (
                SELECT student_id FROM enrollments WHERE schedule_id = %s
            )
        """
        cursor.execute(query, (teacher_id, schedule_id))
        student_lists = cursor.fetchall()
        
        #for table
        cursor.execute("SELECT * FROM enrollments")
        students = cursor.fetchall()
        cursor.close() 
        print(students)
        return render_template("user/sched_class_list.html", student_lists=student_lists,students=students, schedule_id=schedule_id)
    else:
        return not_logged()
#<----actions---->
@app.route('/login_teacher', methods=["POST","GET"])
def login_teacher():
    if request.method == "POST":
        teacher_id =int(request.form["teacher_id"])
        teacher_pass =str(request.form["teacher_pass"])
        
        cursor,conn = get_db_cursor()
        cursor.execute('SELECT * FROM teacher_account WHERE teacher_ID=%s and teacher_password = %s',(teacher_id,teacher_pass))
        valid_teacher=cursor.fetchone()
        if valid_teacher:
            session["teacher_id"]=teacher_id
            session["teacher_pass"]=teacher_pass
            session["teacher_name"]=valid_teacher[1]
            session["logged_in"]=True
            cursor.execute('SELECT * FROM teacher_account WHERE teacher_ID=%s',(session.get('teacher_id')))
            logged_teacher=cursor.fetchall()
            if session.get('logged_in')==True:
                session["logged_teacher"]=logged_teacher
                return render_template("user/index.html",logged_teacher=logged_teacher)
            else:
                flash('Log In Failed', 'error')
                return redirect(url_for('login_teacher_form'))
        else:
            flash('No Account Found', 'error')
            return redirect(url_for('login_teacher_form'))
    else:
        flash('You are not logged in, Session failed!', 'error')
        return redirect(url_for('index'))

@app.route('/add_schedule',methods=["POST", "GET"])
def add_schedule():
    cursor, conn = get_db_cursor()
    if request.method == "POST":
        classGradeLevel = str(request.form["classGradeLevel"])
        class_section = str(request.form["class_section"])
        class_subject = str(request.form["class_subject"])
        class_schedule = str(request.form["class_schedule"])
        class_start_time = str(request.form["class_start_time"])
        class_end_time = str(request.form["class_end_time"])
        number_of_students=0
        teacher=str(session.get('teacher_name'))
        teacher_id=int(session.get('teacher_id'))
            
        query = """
            INSERT INTO class_schedules (
                `grade_level`, 
                `section`, 
                `subject`, 
                `schedule`, 
                `start_time`, 
                `end_time`, 
                `number_of_students`, 
                `teacher`,
                `teacher_id`
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values=(classGradeLevel,class_section,class_subject,class_schedule,class_start_time,class_end_time,number_of_students,teacher,teacher_id)    
        cursor.execute(query,values)
        conn.commit()
        return redirect('/class_schedules')

@app.route('/enroll_student',methods=["POST", "GET"])
def enroll_student():
    cursor, conn = get_db_cursor()
    if request.method == "POST":
        student_id = request.form['student_id']
        student_first_name = request.form['student_first_name']
        student_middle_name = request.form['student_middle_name']
        student_last_name = request.form['student_last_name']
        student_suffix = request.form['student_suffix']
        student_age = request.form['student_age']
        student_guardian = request.form['student_guardian']
        guardian_contact = request.form['guardian_contact']
        teacher_id=int(session.get('teacher_id'))
        
            # Ensure the name is safe for filename
        filename = f"{student_id}.jpg"
        image_path = os.path.join(SAVE_DIR, filename)  # full path where image will be saved

        # Open webcam
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 2)
            height, width = frame.shape[:2]

            # Define the center rectangle (ROI) where user should align their face
            box_width, box_height = 300, 300
            x1 = width // 2 - box_width // 2
            y1 = height // 2 - box_height // 2
            x2 = x1 + box_width
            y2 = y1 + box_height

            # Draw the rectangle frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, "Align face inside box. Press 's' to save.",
                        (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)


            cv2.imshow("Press 's' to Save, 'q' to Quit", frame)

            key = cv2.waitKey(1)
            if key == ord('s'):
                cursor.execute('SELECT * FROM `student_info` WHERE student_id = %s AND teacher_id = %s', (student_id, teacher_id))
                student_exist = cursor.fetchall()
                
                if student_exist:
                    flash('Student Enrolled already', 'error')
                    return redirect(url_for('enrollStudentform'))
                else:
                    cropped_face = frame[y1:y2, x1:x2]
                    if os.path.exists(image_path):
                        print(f"Image already exists at: {image_path}")
                    else:
                        cv2.imwrite(image_path, cropped_face)
                        print(f"Image saved at: {image_path}")
                    
                    image_path_for_db = image_path.replace("\\", "/") #path to be stored in db
                    
                    query = """ 
                        INSERT INTO `student_info`(
                            `student_id`, 
                            `student_image_path`, 
                            `student_first_name`, 
                            `student_middle_name`, 
                            `student_last_name`, 
                            `student_suffix`, 
                            `student_age`, 
                            `student_guardian`, 
                            `guardian_contact`,
                            `teacher_id`
                        ) 
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """
                    values = (student_id, image_path_for_db, student_first_name, student_middle_name, student_last_name, student_suffix, student_age, student_guardian, guardian_contact,teacher_id)
                    
                    cursor.execute(query,values)
            
                    conn.commit()
                    cursor.close()
                    flash('Student Enrolled Successfully', 'success')
                    return redirect(url_for('enrollStudentform'))

            elif key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        
        return redirect(url_for('enrollStudentform'))

@app.route("/take_attendance", methods=["POST", "GET"])
def take_attendance():
    import os
    import cv2
    import numpy as np
    import face_recognition

    known_faces_dir = str(SAVE_DIR)
    known_face_encodings = []
    known_face_names = []

    # Load known faces
    for filename in os.listdir(known_faces_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            path = os.path.join(known_faces_dir, filename)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(os.path.splitext(filename)[0])

    # Start webcam
    video_capture = cv2.VideoCapture(0)
    video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    process_every_n_frames = 3
    frame_count = 0

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        frame = cv2.flip(frame, 2)
        name = "Unknown"

        if frame_count % process_every_n_frames == 0:
            # Resize and convert to RGB
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Detect faces
            face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(distances)
                match = distances[best_match_index] < 0.45

                if match:
                    name = known_face_names[best_match_index]
                    color = (0, 255, 0)
                else:
                    name = "Unknown"
                    color = (0, 0, 255)

                # Scale back to original size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                face_height = bottom - top
                suggestion = ""
                if face_height < 60:
                    suggestion = "Come Closer"
                elif face_height > 180:
                    suggestion = "Move Back"

                # Draw rectangle and label
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6),
                            cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

                if suggestion:
                    cv2.putText(frame, suggestion, (left, top - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        frame_count += 1
        cv2.imshow("Attendance - Press Q to exit", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return "Attendance session ended."





@app.route("/search_students")
def search_students():
    query = request.args.get("query", "")
    teacher_id = session.get('teacher_id')
    
    cursor, conn = get_db_cursor()
    sql = """
        SELECT student_id, student_first_name, student_middle_name, student_last_name
        FROM student_info
        WHERE teacher_id = %s AND student_id LIKE %s
        ORDER BY student_last_name
    """
    cursor.execute(sql, (teacher_id, f"%{query}%"))
    students = cursor.fetchall()
    cursor.close()

    # Convert to JSON format
    student_data = [
        {
            "student_id": student[0],
            "first_name": student[1],
            "middle_name": student[2],
            "last_name": student[3]
        }
        for student in students
    ]

    return jsonify(student_data)
 
 
@app.route('/add_student_tosched/<int:schedule_id>', methods=['POST'])
def add_student_tosched(schedule_id):
    selected_ids = request.form.getlist('student_ids')  # list of selected student_ids

    cursor, conn = get_db_cursor()

    for student_id in selected_ids:
        # Check if already enrolled
        cursor.execute("SELECT * FROM enrollments WHERE student_id = %s AND schedule_id = %s", (student_id, schedule_id))
        if not cursor.fetchone():
            # Get student full name from student_info
            cursor.execute("""
                SELECT student_first_name, student_middle_name, student_last_name
                FROM student_info
                WHERE student_id = %s
            """, (student_id,))
            result = cursor.fetchone()
            if result:
                first_name, middle_name, last_name = result
                full_name = f"{first_name} {middle_name} {last_name}".strip()
                print(full_name)
                # Insert with full name
                cursor.execute("""
                    INSERT INTO enrollments (student_id, schedule_id, student_name)
                    VALUES (%s, %s, %s)
                """, (student_id, schedule_id, full_name))
    
    conn.commit()
    cursor.close()

    return redirect(url_for('view_students_by_schedule', schedule_id=schedule_id))




#admin
@app.route('/admin_home', methods=["POST", "GET"])
def admin_home():
    return render_template("admin/index.html")

@app.route('/sign_out')
def sign_out():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
    