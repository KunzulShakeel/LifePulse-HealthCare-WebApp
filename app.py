from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# ---------- DATABASE SETUP ----------
def init_db():
    with sqlite3.connect('lifepulse.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

# Call DB initialization
init_db()

# ---------- ROUTES ----------

@app.route('/')
def home():
    return redirect(url_for('patient_login'))

@app.route('/patient-login', methods=['GET', 'POST'])
def patient_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        with sqlite3.connect('lifepulse.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM patients WHERE email=? AND password=?", (email, password))
            user = c.fetchone()

        if user:
            session['email'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('patient_dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
            return render_template('patient-login.html')

    return render_template('patient-login.html')

@app.route('/patient-dashboard')
def patient_dashboard():
    if 'email' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('patient_login'))
    return render_template('patient-dashboard.html', email=session['email'])


@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('patient_login'))

@app.route('/patient-register', methods=['GET', 'POST'])
def patient_register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with sqlite3.connect('lifepulse.db') as conn:
            c = conn.cursor()
            try:
                c.execute("INSERT INTO patients (email, password) VALUES (?, ?)", (email, password))
                conn.commit()
                flash('Registration successful! You can now log in.', 'success')
                return redirect(url_for('patient_login'))
            except sqlite3.IntegrityError:
                flash('Email already exists. Please use a different one.', 'error')

    return render_template('patient-register.html')

# ✅ Online Consultation Patient with AI Recommendation
@app.route('/onlineconsultantpatient', methods=['GET', 'POST'])
def online_consultant_patient():
    recommended_doctor = None

    if request.method == 'POST':
        concern = request.form['message'].lower()

        if any(word in concern for word in ["fever", "flu", "cold", "cough"]):
            recommended_doctor = "Dr. Kamran (General Physician)"
        elif any(word in concern for word in ["chest pain", "heart"]):
            recommended_doctor = "Dr. Ayesha (Cardiologist)"
        elif any(word in concern for word in ["headache", "migraine", "dizziness", "numbness"]):
            recommended_doctor = "Dr. Fatima (Neurologist)"
        elif any(word in concern for word in ["rash", "acne", "skin", "skin infection"]):
            recommended_doctor = "Dr. Imran (Dermatologist)"
        elif any(word in concern for word in ["bone pain", "fracture"]):
            recommended_doctor = "Dr. Usman (Orthopedic)"
        elif any(word in concern for word in ["ear", "throat", "nose"]):
            recommended_doctor = "Dr. Hina (ENT Specialist)"
        elif any(word in concern for word in ["depression", "anxiety"]):
            recommended_doctor = "Dr. Bilal (Psychiatrist)"
        elif any(word in concern for word in ["stomach ache", "vomiting"]):
            recommended_doctor = "Dr. Sara (Gastroenterologist)"
        elif any(word in concern for word in ["breathing problem", "asthma"]):
            recommended_doctor = "Dr. Nadia (Pulmonologist)"
        elif any(word in concern for word in ["urinary issue", "urine problem"]):
            recommended_doctor = "Dr. Faisal (Urologist)"
        else:
            recommended_doctor = "Dr. Kamran (General Physician)"

    return render_template('onlineconsultantpatient.html', recommended_doctor=recommended_doctor)



@app.route("/consult")
def consult():
    return render_template("onlineconsultantpatient.html")


@app.route('/schedule-consultation', methods=['POST'])
def schedule_consultation():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    doctor = request.form['doctor']
    date = request.form['date']
    time = request.form['time']
    message = request.form['message']

    print(f'Appointment Request: {name}, {email}, {phone}, {doctor}, {date}, {time}, {message}')

    flash('Your consultation has been scheduled!', 'success')
    return redirect(url_for('patient_dashboard'))

@app.route('/patient-report')
def patient_report():
    return render_template('patientreport.html')

@app.route('/editprofilepatient')
def edit_profile_patient():
    return render_template('editprofilepatient.html')

@app.route('/update-profile', methods=['POST'])
def update_profile():
    return redirect(url_for('patient_dashboard'))

@app.route('/patientappoinment')
def patient_appointment():
    return render_template('patientappoinment.html')

@app.route('/patientmessage')
def patient_message():
    return render_template('patientmessage.html')

@app.route('/patientvideocall')
def patient_video_call():
    return render_template('patientvideocall.html')

@app.route('/welcomepage.html')
def welcome_page():
    return render_template('optio.html')

# ---------- START SERVER ----------
if __name__ == '__main__':
    app.run(debug=True)
