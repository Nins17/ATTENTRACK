from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
from flaskext.mysql import MySQL
import os
import csv
import numpy as np
import cv2
from datetime import datetime

# Create Blueprint
admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")

# MySQL is configured in main.py
mysql = MySQL()

SAVE_DIR = 'static/known_faces'
os.makedirs(SAVE_DIR, exist_ok=True)

#for csv file 
datetoday = datetime.now().strftime("%m_%d_%y")  
CSV_DIR = 'static/attendance_csv'
os.makedirs(CSV_DIR, exist_ok=True)

def get_db_cursor():
    conn = mysql.connect()
    cursor = conn.cursor()
    return cursor, conn
def not_logged():
    flash('Log in as admin first', 'error')
    return redirect(url_for('login_admin_form'))



########## ADMIN SIDE ##########

@admin.route('/login_admin_form', methods=["POST", "GET"])#login for admin PAGE
def login_admin_form():
    return render_template("admin/forms/admin_login_page.html")

@admin.route('/admin_home', methods=["POST","GET"])
def admin_home():
    if session.get('admin_logged_in')==True:
        logged_admin= session.get('logged_admin')
        return render_template("admin/admin_index.html",logged_admin=logged_admin)
    else:
        return not_logged()

@admin.route('/login_admin', methods=["POST","GET"])
def login_admin():
    if request.method == "POST":
        admin_id =request.form.get("admin_id","").strip()
        admin_pass =request.form.get("admin_pass","").strip()
        
        cursor,conn = get_db_cursor()
        cursor.execute('SELECT * FROM admin_account WHERE admin_ID=%s and admin_password = %s',(admin_id,admin_pass))
        valid_admin=cursor.fetchone()
        if valid_admin:
            session["admin_id"]=admin_id
            session["admin_pass"]=admin_pass
            session["admin_name"]=valid_admin[1]
            session["admin_logged_in"]=True
            cursor.execute('SELECT * FROM admin_account WHERE admin_ID=%s',(session.get('admin_id')))
            logged_admin=cursor.fetchall()
            if session.get('admin_logged_in')==True:
                session["logged_admin"]=logged_admin
                return redirect(url_for('admin.admin_home'))
            else:
                flash('Log In Failed', 'error')
                return redirect(url_for('admin.login_admin_form'))
        else:
            flash('Oops! No Account found.', 'error')
            return redirect(url_for('admin.login_admin_form'))
    else:
        flash('You are not logged in as Admin, Session failed!', 'error')
        return redirect(url_for('index'))

@admin.route('/enrollStudentform',methods=["POST", "GET"])
def enrollStudentform():
    if session.get('admin_logged_in')==True:
        
        cursor, conn = get_db_cursor()
        cursor.execute("SELECT DISTINCT grade_level FROM class_schedules")
        avail_grade_level = [row[0] for row in cursor.fetchall()]
 
        # cursor.execute('SELECT DISTINCT section FROM class_schedules WHERE teacher_id=%s',(session.get('teacher_id')))
        # avail_section = [row[0] for row in cursor.fetchall()]
        # print(avail_section)
        # cursor.execute('SELECT DISTINCT subject FROM class_schedules WHERE teacher_id=%s',(session.get('teacher_id')))
        # avail_subject = [row[0] for row in cursor.fetchall()]
        # print(avail_subject)
        return render_template("admin/forms/enroll_student_form.html",grade_level=avail_grade_level)
        #,avail_grade_level=avail_grade_level,avail_section=avail_section,avail_subject=avail_subject,logged_teacher=logged_teacher

        # if avail_grade_level or avail_section or avail_subject :
            
        # else:
        #     pass
    else:
        return not_logged()
 

@admin.route("/enroll_student", methods=["POST", "GET"])
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
        student_gradelevel = request.form['current_gradelevel']
        student_section = request.form['section']

        # Check if student already exists in DB
        cursor.execute('SELECT * FROM student_info WHERE student_id = %s', [student_id])
        student_exist = cursor.fetchone()
        if student_exist:
            flash('Student already enrolled.', 'error')
            return redirect(url_for('admin.enrollStudentform'))

        # Create a folder for this student (e.g. known_faces/101/)
        student_dir = os.path.join(SAVE_DIR, str(student_id))
        if not os.path.exists(student_dir):
            os.makedirs(student_dir)

        # Open webcam
        cap = cv2.VideoCapture(0)
        photo_count = 0
        max_photos = 3  # capture up to 3 faces

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 2)
            height, width = frame.shape[:2]
            box_width, box_height = 300, 300
            x1 = width // 2 - box_width // 2
            y1 = height // 2 - box_height // 2
            x2 = x1 + box_width
            y2 = y1 + box_height

            # Draw the face box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"Align face inside box. ({photo_count}/{max_photos})",
                        (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(frame, "Press 's' to Save | 'q' to Quit", (x1, y2 + 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

            cv2.imshow("Student Enrollment", frame)
            key = cv2.waitKey(1)

            if key == ord('s'):
                cropped_face = frame[y1:y2, x1:x2]

                # Save image as 1.jpg, 2.jpg, 3.jpg
                filename = f"{photo_count + 1}.jpg"
                image_path = os.path.join(student_dir, filename)
                cv2.imwrite(image_path, cropped_face)
                print(f"Saved {image_path}")
                photo_count += 1

                if photo_count >= max_photos:
                    print("Collected enough images.")
                    break

            elif key == ord('q'):
                flash("Enrollment canceled by user.")
                break

        cap.release()
        cv2.destroyAllWindows()

        # If at least one photo was saved, save info to database
        if photo_count > 0:
            first_image_path = os.path.join(student_dir, "1.jpg").replace("\\", "/")
            query = """
                INSERT INTO student_info(
                    student_id, student_image_path, student_first_name, student_middle_name,
                    student_last_name, student_suffix, student_age, student_guardian,
                    guardian_contact, current_grade_level, section
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            values = (
                student_id, first_image_path, student_first_name, student_middle_name,
                student_last_name, student_suffix, student_age, student_guardian,
                guardian_contact, student_gradelevel, student_section
            )
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            flash(f'Student {student_first_name} enrolled successfully with {photo_count} face images.', 'success')
        else:
            flash('No images were captured. Enrollment incomplete.', 'error')

        return redirect(url_for('admin.enrollStudentform'))

    return redirect(url_for('admin.student_list'))

    
@admin.route('/getSection_forEnroll', methods=["POST"])
def getSection_forEnroll():
    grade_level = request.form['current_gradelevel'] 
    cursor, conn = get_db_cursor()
    cursor.execute("SELECT DISTINCT section FROM class_schedules WHERE grade_level=%s", [grade_level])
    sections = cursor.fetchall()
    return jsonify(sections)
 
@admin.route('/registerteacherform',methods=["POST", "GET"])
def registerteacherform():
    if session.get('admin_logged_in')==True:
        # logged_teacher= session.get('logged_admin')
        photo = request.args.get('photo')  # GET photo from camera
        return render_template("admin/forms/register_teacher_form.html",photo=photo)
    else:
        return not_logged()

@admin.route('/register_teacher', methods=['POST'])
def register_teacher():
    cursor, conn = get_db_cursor()

    teacher_id = request.form.get('teacher_id')
    teacher_fname = request.form.get('teacher_first_name')
    teacher_mname = request.form.get('teacher_middle_name')
    teacher_lname = request.form.get('teacher_last_name')
    teacher_suffix = request.form.get('teacher_suffix')
    teacher_default_pass = teacher_id # default password

    cursor.execute("SELECT teacher_ID FROM teacher_accounts WHERE teacher_ID = %s", (teacher_id,))
    teacher_exist =cursor.fetchone()
    if teacher_exist:
        flash(f"Teacher already exists!", 'error')
        return redirect(url_for('admin.registerteacherform'))
    else:
        # photo capture/hidden input
        camera_photo = request.form.get('captured_photo')  # e.g. "20250114_153000.jpg"

        # uploaded photo 
        uploaded_file = request.files.get('teacher_photo')

        final_photo = None
        UPLOAD_FOLDER = 'static/ADMIN/teacher_profpic'

        if camera_photo:
            # Full path of the captured photo
            original_path = os.path.join(UPLOAD_FOLDER, camera_photo)
            
            if os.path.exists(original_path):
                # Keeping original extension
                _, ext = os.path.splitext(camera_photo)
                # Rename using teacher_id
                new_filename = f"{teacher_id}{ext}"
                new_path = os.path.join(UPLOAD_FOLDER, new_filename)
                
                # Rename the saved file in folder
                os.rename(original_path, new_path)
                final_photo = new_path
        elif uploaded_file and uploaded_file.filename != "":
            # Save uploaded photo manually
            photo_ext = uploaded_file.filename.rsplit('.', 1)[1]
            photo_filename = f"{teacher_id}.{photo_ext}"
            upload_path = os.path.join(UPLOAD_FOLDER, photo_filename)
            uploaded_file.save(upload_path)
            final_photo = upload_path

        
        query = """
            INSERT INTO teacher_accounts(
                teacher_ID, teacher_fname, teacher_mname, teacher_lname,
                teacher_suffix, teacher_password, teacher_profile
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            teacher_id, teacher_fname, teacher_mname, teacher_lname,
            teacher_suffix, teacher_default_pass, final_photo
        ))
        conn.commit()

        flash('Teacher Successfully Registered!', 'success')
        return redirect(url_for('admin.registerteacherform'))

@admin.route('/registered_teacher_list') #list of all teachers
def registered_teacher_list():
    if session.get('admin_logged_in')==True:
        cursor, conn = get_db_cursor()
       
        query = """
            SELECT *
            FROM teacher_accounts
        """
        cursor.execute(query)
        registered_teacher_lists = cursor.fetchall()
        
        cursor.close() 
      
        return render_template("admin/registered_teacher_list.html", registered_teacher_lists=registered_teacher_lists)
    else:
        return not_logged()

@admin.route('/update_teacher_form/<int:teacher_id>',methods=["POST", "GET"])
def update_teacher_form(teacher_id):
    if session.get('admin_logged_in')==True:
        session['update_teacher_id'] = teacher_id
        cursor, conn = get_db_cursor()
        photo = request.args.get('photo')
       
        query = """
            SELECT *
            FROM teacher_accounts
            WHERE teacher_id =%s
        """
        cursor.execute(query,(teacher_id))
        teacher_info = cursor.fetchone()
        
        cursor.close() 
      
        return render_template("admin/forms/update_teacher_form.html",teacher_info=teacher_info, photo = request.args.get('photo'))
    else:
        return not_logged()

@admin.route('/update_teacher', methods=['POST'])
def update_teacher():
    if not session.get('admin_logged_in'):
        return not_logged()

    teacher_id = session.get('update_teacher_id')
    if not teacher_id:
        flash("No teacher selected for update.", "error")
        return redirect(url_for('admin.teacherlist'))

    cursor, conn = get_db_cursor()

    # Get form data
    new_teacher_id =request.form.get('teacher_id')
    teacher_fname = request.form.get('teacher_first_name')
    teacher_mname = request.form.get('teacher_middle_name')
    teacher_lname = request.form.get('teacher_last_name')
    teacher_suffix = request.form.get('teacher_suffix')
        
    UPLOAD_FOLDER = 'static/ADMIN/teacher_profpic'
    if new_teacher_id:
        old_photo_path = os.path.join(UPLOAD_FOLDER, f"{teacher_id}.jpg")
        new_TI_filename = f"{new_teacher_id}.jpg"
        new_TI_path = os.path.join(UPLOAD_FOLDER, new_TI_filename)
        os.rename(old_photo_path, new_TI_path)
        
            
    camera_photo = request.form.get('captured_photo')
    uploaded_file = request.files.get('teacher_photo')

    
    final_photo = f"static/ADMIN/teacher_profpic/{new_TI_filename}"

    # If camera photo exists, rename it with teacher ID
    if camera_photo:
    # Full path of the captured photo
        original_path = os.path.join(UPLOAD_FOLDER, camera_photo)

        if os.path.exists(original_path):
            # Delete any existing teacher photo with any extension
            for ext in ["jpg", "jpeg", "png", "gif"]:
                old_photo = os.path.join(UPLOAD_FOLDER, f"{teacher_id}.{ext}")
                if os.path.exists(old_photo):
                    os.remove(old_photo)

            # Rename the captured photo to teacher_id.jpg
            new_filename = f"{new_teacher_id}.jpg"
            new_path = os.path.join(UPLOAD_FOLDER, new_filename)
            os.rename(original_path, new_path)

            final_photo = f"static/ADMIN/teacher_profpic/{new_filename}"

    # If manually uploaded photo
    elif uploaded_file and uploaded_file.filename != "":
        photo_ext = uploaded_file.filename.rsplit('.', 1)[1]
        photo_filename = f"{new_teacher_id}.{photo_ext}"
        upload_path = os.path.join(UPLOAD_FOLDER, photo_filename)
        uploaded_file.save(upload_path)
        final_photo = f"static/ADMIN/teacher_profpic/{photo_filename}"

  
    cursor.execute("""
        UPDATE teacher_accounts
        SET teacher_id=%s,
            teacher_fname = %s,
            teacher_mname = %s,
            teacher_lname = %s,
            teacher_suffix = %s,
            teacher_profile = COALESCE(%s, teacher_profile)
        WHERE teacher_id = %s
    """, ( int(new_teacher_id),teacher_fname, teacher_mname, teacher_lname, teacher_suffix,
       final_photo, teacher_id
    ))
    cursor.execute("""
        UPDATE class_schedules
        SET teacher_id=%s
        WHERE teacher_id = %s
    """, ( int(new_teacher_id),teacher_id))

    conn.commit()
    cursor.close()

    flash("Teacher information updated successfully!", "success")
    return redirect(url_for('admin.registered_teacher_list'))

@admin.route('/remove_teacher_confirmation/<int:teacher_id>')
def remove_teacher_confirmation(teacher_id):
    if session.get('admin_logged_in')==True:
        cursor,conn = get_db_cursor()
        cursor.execute('SELECT * FROM teacher_accounts WHERE teacher_id = %s',[teacher_id])
        teacher_info=cursor.fetchone()
        
        if teacher_info:
            return render_template("admin/remove_teacher_confirmation.html",teacher_info=teacher_info)
        else:
            flash("cant find teacher",'error')
            return redirect(url_for('admin.registered_teacher_list'))
    else:
        return not_logged()
    
@admin.route('/remove_teacher/<int:teacher_id>',  methods=["POST", "GET"])
def remove_teacher(teacher_id):
    if request.method == "POST":
        cursor,conn = get_db_cursor()
        cursor.execute('SELECT * FROM teacher_accounts WHERE teacher_id = %s',[teacher_id])
        teacher=cursor.fetchone()
        
        if teacher:
            file_path = teacher[1]  
            full_path = os.path.join('static/files', file_path)  
            
            # Delete the photo in path
            if os.path.exists(full_path):
                os.remove(full_path)
                
        
        cursor.execute("DELETE FROM teacher_accounts WHERE teacher_id = %s", (teacher_id,))
        conn.commit()
        
        
        flash("Teacher Removed",'ERROR')
        cursor.close()
        return redirect(url_for('admin.registered_teacher_list'))
    
@admin.route('/add_schedule_page',methods=["POST", "GET"])
def add_schedule_page():
    if session.get('admin_logged_in')==True:
        cursor, conn = get_db_cursor()
        query = """
            SELECT *
            FROM teacher_accounts
        """
        cursor.execute(query)
        registered_teachers = cursor.fetchall()
        return render_template("admin/forms/add_schedule_form.html",teacher_list=registered_teachers)
    else:
        return not_logged()
    
@admin.route('/add_schedule',methods=['POST','GET'])
def add_schedule():
    cursor, conn = get_db_cursor()
    if request.method == "POST":
        class_gradeLevel = str(request.form.get("classGradeLevel"))
        class_section = str(request.form.get("class_section"))
        class_subject = str(request.form.get("class_subject"))
        class_schedule = str(request.form.get("class_schedule"))
        class_start_time = str(request.form.get("class_start_time"))
        class_end_time = str(request.form.get("class_end_time"))
        teacher_id = int(request.form.get("teacher_id"))

        cursor.execute('SELECT * FROM teacher_accounts WHERE teacher_ID = %s', (teacher_id,))
        teacher_info = cursor.fetchone()
        teacher_name = f"{teacher_info[4]}, {teacher_info[2]} {teacher_info[3]} {teacher_info[5]}"
        number_of_students = 0

        check_sched = """
            SELECT * FROM class_schedules
            WHERE grade_level = %s
            AND section = %s
            AND subject = %s
            AND schedule = %s
            AND start_time = %s
            AND end_time = %s
        """
        cursor.execute(check_sched, (class_gradeLevel, class_section, class_subject, class_schedule, class_start_time, class_end_time))
        existing_sched = cursor.fetchone()
        if existing_sched:
            flash("Class schedule already exists.", "warning")
        else:
            query="""INSERT INTO class_schedules(schedule_id,
                    grade_level, section, subject,schedule,
                    start_time, end_time, number_of_students,teacher,teacher_id
                ) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            values=(0,class_gradeLevel, class_section, class_subject, class_schedule, class_start_time, class_end_time,number_of_students,teacher_name,teacher_id)
            cursor.execute(query,values)
            conn.commit()
            cursor.close()
            flash("Class schedule successfully Added", "success")
        return redirect(url_for('admin.add_schedule_page'))    
    else:    
        flash("Failed Request", "error")
        return redirect(url_for('admin.add_schedule_page'))    
 
@admin.route('/update_sched_form/<int:sched_id>', methods=["POST", "GET"])
def update_sched_form(sched_id):
    if session.get('admin_logged_in')==True:
        session["update_sched_id"] = sched_id
        cursor,conn = get_db_cursor()
        cursor.execute('SELECT * FROM class_schedules WHERE schedule_id = %s',[sched_id])
        sched=cursor.fetchone()
        print(sched)
        cursor.execute('SELECT teacher_lname, teacher_fname, teacher_mname, teacher_suffix FROM teacher_accounts WHERE teacher_id = %s',(sched[9],))
        teacher_info=cursor.fetchone()
        teacher_name = f"{teacher_info[0]}, {teacher_info[1]} {teacher_info[2]} {teacher_info[3]}"
        print(teacher_name)
        cursor.execute('SELECT * FROM teacher_accounts')
        selection_teacher=cursor.fetchall()
        session["update_sched_teacher_id"] = sched[9]
        print(selection_teacher)
        
        
        if sched:
            return render_template("admin/forms/update_schedule_form.html",sched=sched, teacher_name=teacher_name,selection_teacher=selection_teacher)
    else:
        return not_logged()  
    
@admin.route('/update_sched', methods=["POST", "GET"])
def update_sched():
    cursor, conn = get_db_cursor()
    if request.method == "POST":
        class_gradeLevel = str(request.form.get("classGradeLevel"))
        class_section = str(request.form.get("class_section"))
        class_subject = str(request.form.get("class_subject"))
        class_schedule = str(request.form.get("class_schedule"))
        class_start_time = str(request.form.get("class_start_time"))
        class_end_time = str(request.form.get("class_end_time"))
        teacher_id = int(request.form.get("teacher_id"))

        cursor.execute('SELECT * FROM teacher_accounts WHERE teacher_ID = %s', (teacher_id,))
        teacher_info = cursor.fetchone()
        teacher_name = f"{teacher_info[4]}, {teacher_info[2]} {teacher_info[3]} {teacher_info[5]}"
        

        check_sched = """
            SELECT * FROM class_schedules
            WHERE schedule_id =%s
        """
        cursor.execute(check_sched, (session.get('update_sched_id'),))
        existing_sched = cursor.fetchone()
        if existing_sched:
            query = """
                    UPDATE class_schedules
                    SET
                        grade_level = %s,
                        section = %s,
                        subject = %s,
                        schedule = %s,
                        start_time = %s,
                        end_time = %s,
                        teacher = %s,
                        teacher_id = %s
                    WHERE schedule_id = %s
                """
            values=(class_gradeLevel, class_section, class_subject, class_schedule, class_start_time, class_end_time,teacher_name,teacher_id, session.get('update_sched_id'))
            cursor.execute(query,values)
            conn.commit()
            cursor.close()
            flash("Class schedule successfully Updated", "success")
            return redirect(url_for('admin.update_sched_form',sched_id = session.get('update_sched_id')))    
        else:    
            flash("Schedule Update Failed", "error")
            return redirect(url_for('admin.update_sched_form',sched_id = session.get('update_sched_id'))) 
    else:    
        flash("Failed Request", "error")
        return redirect(url_for('admin.update_sched_form',sched_id = session.get('update_sched_id')))    
    
@admin.route('/class_schedule_list')#list of all schedules
def class_schedule_list():
    if session.get('admin_logged_in')==True:
        cursor, con = get_db_cursor()
        cursor.execute('SELECT * FROM class_schedules;')
        class_schedule_list = cursor.fetchall()
        print(class_schedule_list)
        return render_template("admin/class_schedule_list_page.html", schedule_list = class_schedule_list)
    else:
        return not_logged()         
 
@admin.route('/add_student_to_sched_page/<int:sched_id>')
def add_student_to_sched_page(sched_id):
    if session.get('admin_logged_in')==True:
        cursor,conn = get_db_cursor()
        cursor.execute("SELECT * FROM class_schedules WHERE schedule_id=%s", (sched_id,))
        fetched_sched = cursor.fetchone()
        current_grade_level= fetched_sched[1]
        
        query = """
            SELECT *
            FROM student_info WHERE current_grade_level=%s 
        """
        cursor.execute(query,(current_grade_level))
        student_lists = cursor.fetchall()
        return render_template("admin/forms/add_student_to_sched_form.html",sched_info=fetched_sched, students=student_lists)
    else:
        return not_logged()
    
@admin.route('/add_student_to_sched/<int:sched_id>', methods=['POST','GET'])
def add_student_to_sched(sched_id):
    selected_ids = request.form.getlist('selected_students')  # list of selected student_ids

    cursor, conn = get_db_cursor()
    cursor.execute("SELECT teacher_id FROM class_schedules WHERE schedule_id = %s", (sched_id,))
    result = cursor.fetchone()

    if result:
        teacher_id = result[0]

    for student_id in selected_ids:
        # Check if already enrolled
        cursor.execute("SELECT * FROM student_schedule_enrollments WHERE student_id = %s AND schedule_id = %s", (student_id, sched_id))
        if not cursor.fetchone():
            # Get student full name from student_info
            cursor.execute("""
                SELECT student_first_name, student_middle_name, student_last_name
                FROM student_info
                WHERE student_id = %s 
            """, (student_id,))
            result = cursor.fetchone()

            if result:
                student_first_name, student_middle_name, student_last_name = result
                full_name = f"{student_first_name} {student_middle_name} {student_last_name}".strip()

                cursor.execute("""
                    INSERT INTO student_schedule_enrollments (student_id, schedule_id, student_name,teacher_id)
                    VALUES (%s, %s, %s, %s)
                """, (student_id, sched_id, full_name,teacher_id))
        else:
            flash("Student Already Added","warning")
           
            
    # Update number_of_students after all inserts
    cursor.execute("""
        UPDATE class_schedules
        SET number_of_students = (
            SELECT COUNT(*)
            FROM student_schedule_enrollments
            WHERE schedule_id = %s
        )
        WHERE schedule_id = %s
    """, (sched_id, sched_id))

    conn.commit()
    cursor.close()

    flash("Adding Students to Schedule Successfull!","success")
    return redirect(url_for('admin.student_by_schedule_list',sched_id=sched_id))

@admin.route('/remove_sched_confirmation/<int:sched_id>')
def remove_sched_confirmation(sched_id):
    if session.get('admin_logged_in')==True:
        cursor,conn = get_db_cursor()
        cursor.execute('SELECT * FROM class_schedules WHERE schedule_id = %s',[sched_id])
        sched=cursor.fetchone()
        
        if sched:
            return render_template("admin/sched_confirmation.html",sched_info=sched)
        else:
            flash("cant find student",'error')
            return redirect(url_for('admin.class_schedule_list'))
    else:
        return not_logged()
    
@admin.route('/remove_sched/<int:sched_id>',  methods=["POST", "GET"])
def remove_sched(sched_id):
    if request.method == "POST":
        cursor,conn = get_db_cursor()
        cursor.execute("DELETE FROM class_schedules WHERE schedule_id = %s", (sched_id,))
        conn.commit()
        
        flash("Schedule Removed",'warning')
        cursor.close()
        return redirect(url_for('admin.class_schedule_list'))
 
@admin.route('/student_by_schedule_list/<int:sched_id>')
def student_by_schedule_list(sched_id):
    if session.get('admin_logged_in')==True:
        cursor, conn = get_db_cursor()
        #list of all students per schedule
        query = """
            SELECT *
            FROM student_schedule_enrollments
            WHERE schedule_id=%s
        """
        cursor.execute(query,(sched_id,))
        student_lists = cursor.fetchall()
        
        cursor.execute("SELECT * FROM class_schedules WHERE schedule_id=%s", (sched_id,))
        fetched_sched = cursor.fetchone()
        
        return render_template("admin/students_by_schedule.html",sched_id=sched_id, student_lists=student_lists, sched_info=fetched_sched)
    else:
        return not_logged()
    
@admin.route('/remove_student_from_sched_confirmation/<int:enrollment_id>')
def remove_student_from_sched_confirmation(enrollment_id):
    if session.get('admin_logged_in')==True:
        cursor,conn = get_db_cursor()
        cursor.execute('SELECT * FROM student_schedule_enrollments WHERE enrollment_id = %s',[enrollment_id])
        student=cursor.fetchone()
        
        if student:
            return render_template("admin/remove_confirmation.html",student_info=student)
        else:
            flash("cant find student",'error')
            return redirect(url_for('admin.student_by_schedule_list',sched_id=student[2]))
    else:
        return not_logged()
    
@admin.route('/remove_student_from_sched/<int:sched_id>/<int:enrollment_id>',  methods=["POST", "GET"])
def remove_student_from_sched(sched_id,enrollment_id):
    if request.method == "POST":
        cursor,conn = get_db_cursor()
        cursor.execute("DELETE FROM student_schedule_enrollments WHERE enrollment_id = %s", (enrollment_id,))
        conn.commit()
        
         # Update number_of_students after all inserts
        cursor.execute("""
            UPDATE class_schedules
            SET number_of_students = (
                SELECT COUNT(*)
                FROM student_schedule_enrollments
                WHERE schedule_id = %s
            )
            WHERE schedule_id = %s
        """, (sched_id, sched_id))

        conn.commit()
        cursor.close()
        
        flash("Student Removed from Schedule",'warning')
        cursor.close()
        return redirect(url_for('admin.student_by_schedule_list',sched_id=sched_id))
    
@admin.route('/attendance_records', methods=["POST", "GET"])
def attendance_records():
    if session.get('admin_logged_in')==True:
        cursor, conn = get_db_cursor()
        cursor.execute("""SELECT a.*, t.teacher_fname,t.teacher_mname,t.teacher_lname,
                        t.teacher_suffix
                        FROM attendance_logs a
                        LEFT JOIN teacher_accounts t
                        ON a.teacher_id = t.teacher_id""")
        csv_files=cursor.fetchall()
        return render_template("admin/attendance_records_admin.html", csv_files=csv_files)
    else:
        return not_logged()
    
@admin.route('/student_list')
def student_list():
    if session.get('admin_logged_in')==True:
        cursor, conn = get_db_cursor()
        #list of all students
        query = """
            SELECT *
            FROM student_info
        """
        cursor.execute(query)
        student_lists = cursor.fetchall()
        
        #for table
        cursor.close() 
      
        return render_template("admin/student_list.html", student_lists=student_lists)
    else:
        return not_logged()
    
@admin.route('/update_student_info_page/<int:student_id>', methods=['POST','GET'])
def update_student_info_page(student_id):
    student_new_photo = request.args.get('student_new_photo')
    cursor,conn = get_db_cursor()
    cursor.execute("SELECT DISTINCT grade_level FROM class_schedules")
    avail_grade_level = [row[0] for row in cursor.fetchall()]
 
    cursor.execute("SELECT * FROM student_info WHERE student_id = %s",[student_id])  
    student = cursor.fetchone()
    return render_template("admin/forms/update_student_info_page.html", student = student, grade_level=avail_grade_level, student_new_photo=student_new_photo)
  
@admin.route('/update_student_info/<int:student_id>', methods=['POST','GET'])
def update_student_info(student_id):
    if request.method == "POST":
        cursor,conn=get_db_cursor()
        # temp_photo_path = request.form.get("new_captured_photo")  
        new_student_first_name = request.form.get("student_first_name")
        new_student_middle_name = request.form.get("student_middle_name")
        new_student_last_name = request.form.get("student_last_name")
        new_student_suffix = request.form.get("student_suffix")
        new_student_age = request.form.get("student_age")
        new_student_guardian = request.form.get("student_guardian")
        new_guardian_contact= request.form.get("guardian_contact")
        new_student_gradelevel = request.form.get("current_gradelevel")
        new_student_section = request.form.get("section")
        
        # if temp_photo_path:
        #     # Remove the "/static/" to change to correct format 
        #     temp_photo_path = temp_photo_path.replace("/static/", "")  
        #     full_old_path = os.path.join("static", temp_photo_path)

        #     # Get the file extension (like ".jpg" or ".png")
        #     _, ext = os.path.splitext(full_old_path)
        #     new_filename = f"{student_id}{ext}"
        #     folder_to_move = os.path.join("static", "known_faces")
        #     new_path = os.path.join(folder_to_move, new_filename)

        #     # Make sure the folder exists
        #     os.makedirs(folder_to_move, exist_ok=True)

        #     # If the temp file exists, move and rename it
        #     if os.path.exists(full_old_path):
        #         if os.path.exists(new_path):
        #             os.remove(new_path) # Delete old photo with the same name to avoid duplicates
        #         os.rename(full_old_path, new_path)
        #         print(" Succesfully moved new photo to:", new_path)
        #         new_image_path_for_db = new_path.replace("\\", "/")
        #     else:
        #         # keeping the current one in the database
        #         print("No changes to image")
        #         cursor.execute("SELECT student_image_path FROM student_info WHERE student_id = %s", (student_id,))
        #         existing_photo = cursor.fetchone()
        #         if existing_photo:
        #             new_image_path_for_db = existing_photo[0]
        #         else:
        #             new_image_path_for_db = None
        # else:
        # No new photo submitted
        # cursor.execute("SELECT student_image_path FROM student_info WHERE student_id = %s", (student_id,))
        # existing_photo = cursor.fetchone()
        # new_image_path_for_db = existing_photo[0] if existing_photo else None
            
        query = """
                UPDATE student_info
                SET 
                    student_first_name = %s,
                    student_middle_name = %s,
                    student_last_name = %s,
                    student_suffix = %s,
                    student_age = %s,
                    student_guardian = %s,
                    guardian_contact = %s,
                    current_grade_level = %s,
                    section = %s
                WHERE student_id = %s
            """

        values = (
            # new_image_path_for_db,
            new_student_first_name,
            new_student_middle_name,
            new_student_last_name,
            new_student_suffix,
            new_student_age,
            new_student_guardian,
            new_guardian_contact,
            new_student_gradelevel,
            new_student_section,
            student_id   # from URL or hidden input
        )

        cursor.execute(query, values)
        conn.commit()
        flash("Student updated successfully!", "success")
        return redirect(url_for('admin.update_student_info_page', student_id=student_id))      

@admin.route('/remove_student_confirmation/<int:student_id>')
def remove_student_confirmation(student_id):
    if session.get('admin_logged_in')==True:
        cursor,conn = get_db_cursor()
        cursor.execute('SELECT * FROM student_info WHERE student_id = %s',[student_id])
        student=cursor.fetchone()
        
        if student:
            file_path = student[1]  
            full_path = os.path.join('static/files', file_path)  
            
            # Delete the photo in path
            if os.path.exists(full_path):
                os.remove(full_path)
                
            return render_template("admin/confirmation.html",student_info=student)
        else:
            flash("cant find student",'error')
            return redirect(url_for('admin.student_list'))
    else:
        return not_logged()
    
@admin.route('/remove_student/<int:student_id>', methods=["POST", "GET"])
def remove_student(student_id):
    if request.method == "POST":
        cursor, conn = get_db_cursor()

        cursor.execute("""
            SELECT DISTINCT schedule_id FROM student_schedule_enrollments WHERE student_id = %s
        """, (student_id,))
        schedule_rows = cursor.fetchall()

        cursor.execute("DELETE FROM student_info WHERE student_id = %s", (student_id,))
        conn.commit()

        student_dir = os.path.join(SAVE_DIR, str(student_id))
        if os.path.exists(student_dir) and os.path.isdir(student_dir):
            for filename in os.listdir(student_dir):
                file_path = os.path.join(student_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            os.rmdir(student_dir)

        for (sched_id,) in schedule_rows:
            cursor.execute("""
                UPDATE class_schedules
                SET number_of_students = (
                    SELECT COUNT(*) FROM student_schedule_enrollments WHERE schedule_id = %s
                )
                WHERE schedule_id = %s
            """, (sched_id, sched_id))
            conn.commit()

        cursor.close()
        flash("Student removed successfully.", "success")
        return redirect(url_for('admin.student_list'))


        
        
                        
####CAMERA ROUTES###
@admin.route('/update_student/camera/<int:student_id>')
def update_studentcamera(student_id):
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        flash("Camera not detected!", "error")
        return redirect(url_for('admin.registerteacherform'))

    while True:
        ret, frame = cam.read()
        if not ret:
            flash("Failed to read from camera.", "error")
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
    
        

        cv2.imshow("Update Student Camera -Press S to Save | Q to Quit", frame)

        key = cv2.waitKey(1) & 0xFF

        # Press 's' to save image
        if key == ord('s'):
            cropped_face = frame[y1:y2, x1:x2]
            photo_filename = datetime.now().strftime("%Y%m%d") + "_tmp.jpg"
            old_photo = os.path.join("static/knownfaces/tmp", photo_filename)
            if os.path.exists(old_photo):
                 os.remove(old_photo)
            
            save_path = os.path.join("static/known_faces/tmp", photo_filename)
            cv2.imwrite(save_path, cropped_face)

            # to be displayed in the front end
            relative_path = f"known_faces/tmp/{photo_filename}"

            return redirect(url_for('admin.update_student_info_page',
                                    student_id=student_id,
                                    student_new_photo=relative_path))
        
        # Press 'q' to quit camera without saving
        elif key == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    return redirect(url_for('admin.update_student_info_page',student_id=student_id))

@admin.route('/teacher/camera')
def teacher_camera():
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        flash("Camera not detected!", "error")
        return redirect(url_for('admin.registerteacherform'))

    while True:
        ret, frame = cam.read()
        frame = cv2.flip(frame, 2)
        if not ret:
            flash("Failed to read from camera.", "error")
            break

        cv2.imshow("Press S to Save | Q to Quit", frame)

        key = cv2.waitKey(1) & 0xFF

        # Press 's' to save image
        if key == ord('s'):
            photo_filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
            save_path = os.path.join("static/ADMIN/teacher_profpic", photo_filename)
            cv2.imwrite(save_path, frame)
            flash("Photo Captured!", "success")
            cam.release()
            cv2.destroyAllWindows()
            return redirect(url_for('admin.registerteacherform', photo=photo_filename))
        
        # Press 'q' to quit camera without saving
        elif key == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    return redirect(url_for('admin.registerteacherform'))

@admin.route('/update_teacher_camera/<int:teacher_id>')
def update_teacher_camera(teacher_id):
    if not session.get('admin_logged_in'):
        return not_logged()

    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        flash("Camera not detected!", "error")
        return redirect(url_for('admin.update_teacher_form', teacher_id=teacher_id))

    while True:
        ret, frame = cam.read()
        frame = cv2.flip(frame, 2)
        if not ret:
            flash("Failed to read from camera.", "error")
            break

        cv2.imshow("Press S to Save | Q to Quit", frame)
        key = cv2.waitKey(1) & 0xFF

        # Press 's' to save image
        if key == ord('s'):
            photo_filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
            save_path = os.path.join("static/ADMIN/teacher_profpic", photo_filename)
            cv2.imwrite(save_path, frame)

            flash("Photo captured successfully!", "success")
            cam.release()
            cv2.destroyAllWindows()

            # Pass captured photo filename to form
            return redirect(url_for('admin.update_teacher_form', teacher_id=teacher_id, photo=photo_filename))
        
        # Press 'q' to quit camera without saving
        elif key == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    flash("Camera closed without saving.", "info")
    return redirect(url_for('admin.update_teacher_form', teacher_id=teacher_id))
