from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import urllib
from sqlalchemy import text
from datetime import datetime


app = Flask(__name__)

pwd = '!@mElv!s@19'
db_name = 'nishauri'

pwd = urllib.parse.quote(pwd)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqldb://root:{pwd}@localhost:3306/{db_name}'

db = SQLAlchemy(app)

@app.route('/appointments')
def getAppointment():
    """Retrieve all the appointements"""
    with db.session.begin():
        query = text('SELECT * FROM Appointments')
        appointments = db.session.execute(query).fetchall()
    
    appointment_list = []
    for appointment in appointments:
        appointment_details = {
            'AppointmentID': appointment[0],
            'PatientID': appointment[1],
            'AppointmentDate': appointment[2],
            # 'AppointmentTime': appointment[3],
            'Doctor': appointment[4],
            'Notes': appointment[5]
        }
        appointment_list.append(appointment_details)
    return jsonify({'appointments': appointment_list})

@app.route('/appointments/<int:id>')
def getDoctorAppointments(id):
    """Retrieve a doctors appointments"""
    with db.session.begin():
        query = text(f'SELECT * FROM Appointments WHERE PatientID={id}')
        appointments = db.session.execute(query).fetchall()
        
    appointment_list = []
        
    for appointment in appointments:
        appointment_details = {
        'AppointmentDate': appointment[2],
        # 'AppointmentTime': appointment[3],
        'Doctor': appointment[4],
        'Notes': appointment[5]
        }
        appointment_list.append(appointment_details)
    return jsonify({"appointments": appointment_list})

@app.route('/medicalHistory/<int:id>')
def getMedicalHistory(id):
    """Retrieve patient medical histroy"""
    with db.session.begin():
        query =  text(f"SELECT * FROM MedicalHistory WHERE PatientID={id}")
        history = db.session.execute(query).fetchall()
    
    history_list = []
    
    for hs in history:
        history_details = {
            'Diagnosis': hs[2],
            'Treatment': hs[3],
            'Date': hs[4]
        }
        history_list.append(history_details)
    
    return jsonify({'MedicalHistory': history_list})

@app.route('/medications/<int:id>')
def getMedications(id):
    """Retrieve the medications the patient is taking"""
    with db.session.begin():
        query = text(f"SELECT * FROM Medications WHERE PatientID={id}")
        medications = db.session.execute(query).fetchall()
    
    medication_list = []
    
    for medication in medications:
        med = {
            "MedicationName": medication[2],
            "Dosage": medication[2],
            "Frequency": medication[3]
        }
        medication_list.append(med)
    return jsonify({"Medications": medication_list})

@app.route('/patients/<string:number>')
def getPatient(number):
    """Retrieve a patient's Details"""
    
    with db.session.begin():
        query = text(f"SELECT * FROM Patients WHERE ContactNumber={number:s}")
        patient = db.session.execute(query).fetchone()
        patient_info = []
        patient_dict = {
            "PatientId": patient[0],
            "FirstName": patient[1],
            "LastName": patient[2],
            "DateOfBirth": patient[3],
            "ContactNumber": patient[4],
            "Address": patient[5]
        }
        patient_info.append(patient_dict)
    return jsonify({"PatientDetails": patient_info})

@app.route("/patients/insuarance/<int:id>")
def getInsuaranceInfo(id):
    with db.session.begin():
        query = text(f"SELECT * FROM Insurance WHERE PatientID={id:d}")
        insurance = db.session.execute(query).fetchone()
    insuranceInfo = []
    insuranceDict = {
        "ProvideName": insurance[2],
        "ExpiryDate": insurance[-1]
    }
    insuranceInfo.append(insuranceDict)
    
    return jsonify({"InsuranceInfo": insuranceInfo})

@app.route('/appoitmentReminders')
def sendApointmentReminders():
    date = datetime.now()

    # Format the date as "YYYY-MM-DD"
    date_today = date.strftime("%Y-%m-%d")
    with db.session.begin():
        query = text('''
            SELECT 
                A.AppointmentID,
                A.AppointmentDate,
                A.AppointmentTime,
                A.Doctor,
                A.Notes,
                A.Type,
                P.ContactNumber AS PatientPhoneNumber,
                P.FirstName As PatientName
            FROM 
                nishauri.Appointments A
            JOIN 
                nishauri.Patients P ON A.PatientID = P.PatientID 
            WHERE 
                AppointmentDate = :date_today
        ''')
        result = db.session.execute(query, {'date_today': date_today}).fetchall()
    
    print(result)
    reminders = []
    for appointment in result:
        phoneNumber = appointment[6]
        doctor = appointment[3]
        date = date_today
        notes = appointment[4]
        appointmentType = appointment[5]
        patientName = appointment[7]
        data =  {
           'phoneNumber': phoneNumber,
           'date': date,
           'notes': notes,
           'doctor': doctor,
           'appointmentType': appointmentType,
           'patientName': patientName
        }
        reminders.append(data)


    return jsonify({"reminders": reminders})
        

if __name__ == '__main__':
    app.run(debug=True)