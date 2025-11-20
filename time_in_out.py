from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
from mysql import mysql
import os
import csv
import numpy as np
import cv2
import face_recognition
from datetime import datetime,time
from message import send_attendance_sms
import base64


# Create Blueprint
time_in_out = Blueprint("time_in_out", __name__, static_folder="static", template_folder="templates")

SAVE_DIR = 'static/known_faces'
os.makedirs(SAVE_DIR, exist_ok=True)

#for csv file 
datetoday = datetime.now().strftime("%m_%d_%y")  
CSV_DIR = 'static/time_in_out__csv'
os.makedirs(CSV_DIR, exist_ok=True)

#inputs
datetoday = datetime.now().strftime("%m_%d_%y") 
yeartoday = datetime.now().year
schoolyear = f"{yeartoday} - {yeartoday+1}"
known_face_encodings = []
known_face_names = []

def get_db_cursor():
    conn = mysql.connect()
    cursor = conn.cursor()
    return cursor, conn


def load_known_faces():
    #Load all student photos and average their encodings per studen.
    global known_face_encodings, known_face_names
    known_face_encodings.clear()
    known_face_names.clear()

    for student_folder in os.listdir(SAVE_DIR):
        student_path = os.path.join(SAVE_DIR, student_folder)
        if not os.path.isdir(student_path):
            continue

        encodings = []
        # Loop through each photo of that student
        for filename in os.listdir(student_path):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(student_path, filename)
                image = face_recognition.load_image_file(img_path)
                face_enc = face_recognition.face_encodings(image)
                if face_enc:
                    encodings.append(face_enc[0])

        if encodings:
            mean_encoding = np.mean(encodings, axis=0)
            known_face_encodings.append(mean_encoding)
            known_face_names.append(student_folder)  # folder name = student_id
load_known_faces()

face_cascade = cv2.CascadeClassifier("static/haarcascade_frontalface_default.xml")
# Load all faces once when app starts
@time_in_out.route('/take_attendance_page', methods=["POST","GET"])
def take_attendance_page():
    return render_template('time_in_out_page.html')

@time_in_out.route("/take_attendance_cam", methods=["POST","GET"])
def take_attendance_cam():
    return render_template("take_attendace_cam.html")



def update_attendance(student_id, student_name):
    cursor, conn = get_db_cursor()
    
    os.makedirs(CSV_DIR, exist_ok=True)
    csv_name = f"TimeIN_OUT({datetoday})_Record.csv"
    csv_path = os.path.join(CSV_DIR, csv_name)
    relative_path = csv_path.replace("\\", "/")

    # Create CSV if not exists
    if not os.path.exists(csv_path):
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date","ID","Name","AM_IN","AM_OUT","PM_IN","PM_OUT","LAST_TIME_OUT"])
          # for Windows backslash
        cursor.execute("""
                INSERT INTO time_in_out_record_paths (record_id, csv_path, date)
                VALUES (%s, %s, %s)
            """, (0, relative_path,datetoday))
        conn.commit()


    # Read current records
    records = []
    found_entry = None
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row and row[1] == str(student_id) and row[0] == datetoday:
                found_entry = row
            records.append(row)

    if not found_entry:
        found_entry = [datetoday, student_id, student_name, "", "", "", "", ""]
        records.append(found_entry)

    # Time slots
    AM_IN, AM_OUT, PM_IN, PM_OUT, LAST_TIME_OUT = 3, 4, 5, 6, 7
    am_start, am_end = time(7,0), time(11,30)
    pm_start, pm_end = time(13,0), time(17,0)
    time_now = datetime.now().time()
    time_now_str = datetime.now().strftime("%H:%M:%S")
    status = ""
    time_out_sms = False

    # AM/PM logic
    if found_entry[AM_IN] == "":
        if time_now <= am_start:
            found_entry[AM_IN] = time_now_str
            status = "AM Time In Early"
            statuscat="ok"
        elif am_start <= time_now <= am_end:
            found_entry[AM_IN] = time_now_str
            status = "Success AM Time In"
            statuscat="ok"
        else:
            found_entry[AM_IN] = "absent"
            found_entry[AM_OUT] = "absent"
            found_entry[PM_IN] = time_now_str
            status = "Missed AM, logged PM Time In"
            statuscat="error"

    elif found_entry[AM_IN] != "" and found_entry[AM_OUT] == "":
        if am_end <= time_now <= pm_start:
            found_entry[AM_OUT] = time_now_str
            status = "Success AM Time Out"
            time_out_sms = True
            statuscat="ok"
        else:
            found_entry[AM_OUT] = f"{time_now_str}(Missed Time Out)"
            found_entry[LAST_TIME_OUT] = time_now_str
            status = f"Last time out AM{time_now_str}"
            statuscat="error"

    elif found_entry[PM_IN] == "":
        if pm_start <= time_now <= pm_end:
            found_entry[PM_IN] = time_now_str
            status = "Success PM Time In"
            statuscat="ok"
            
        else:
            found_entry[PM_IN] = f"{time_now_str} Late"
            status = "PM Time In Late"
            statuscat="error"

    elif found_entry[PM_OUT] == "":
        if pm_start <= time_now <= pm_end:
            found_entry[PM_OUT] = time_now_str
            status = "Succes PM Time Out"
            time_out_sms = True
            statuscat="ok"
        else:
            found_entry[PM_OUT] = time_now_str
            found_entry[LAST_TIME_OUT] = time_now_str
            status = f"Last time out PM{time_now_str}"
            statuscat="ok"
    else:
        status = "Already logged"
        statuscat="error"

    # Save CSV
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date","ID","Name","AM_IN","AM_OUT","PM_IN","PM_OUT","LAST_TIME_OUT"])
        writer.writerows(records)
        
    statusfinal=f"Student Name:{student_name} STATUS: {status} "
    statuscat="ok"

    return statusfinal, time_out_sms, statuscat

# -----------------------------
# Process frame
# -----------------------------
@time_in_out.route("/process_frame", methods=["POST"])
def process_frame():
    try:
        cursor, conn = get_db_cursor()
        data = request.get_json()
        if not data or "img" not in data:
            return jsonify({"status": "No image sent", "faces": []})

        img_b64 = data["img"].split(",")[1]
        frame = cv2.imdecode(np.frombuffer(base64.b64decode(img_b64), np.uint8), cv2.IMREAD_COLOR)

        # Process frame as usual
        small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
        rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small)
        face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

        statusfinal = "No face detected...Scan Again"
        faces_output = []
        statuscat = "error" 

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            name = "Unknown"
            time_out_sms = False

            if True in matches:
                index = matches.index(True)
                student_id = known_face_names[index]

                cursor.execute("""
                    SELECT student_id, student_first_name, student_middle_name,
                           student_last_name, student_suffix, guardian_contact
                    FROM student_info
                    WHERE student_id=%s
                """, (student_id,))
                info = cursor.fetchone()
                if info:
                    student_name = f"{info[3]}, {info[1]} {info[2]} {info[4]}"
                    statusfinal, time_out_sms,statuscat = update_attendance(student_id, student_name)
                    name = student_name
                    if info[5] and time_out_sms:
                        send_attendance_sms(info[5], student_name, datetime.now().strftime("%H:%M:%S"))
            else:
                statusfinal = "Face not recognized"
                statuscat = "error"

            scale = 4
            faces_output.append({
                "x": left*scale,
                "y": top*scale,
                "w": (right-left)*scale,
                "h": (bottom-top)*scale,
                "name": name
            })

        return jsonify({"status": statusfinal, "faces": faces_output,"statuscat":statuscat})
    except Exception as e:
        # Always return JSON even if something breaks
        print("Error in process_frame:", e)
        return jsonify({"status": "Server error: "+str(e), "faces": [], "statuscat":"error"})

   