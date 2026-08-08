import csv
import json
import os
from datetime import datetime


class patient:
    def __init__(self, patient_id, name, age, gender, blood_type, disease=None):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.blood_type = blood_type
        self.disease = disease

    def to_dict(self):
        patient_dict = {
            "patient_id":self.patient_id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "blood_type": self.blood_type,
            "disease": self.disease
        }
        return patient_dict


class doctor:
    def __init__(self, doctor_id, name, specialization, department, username=None, password=None):
        self.doctor_id = doctor_id
        self.name = name
        self.specialization = specialization
        self.department = department
        self.username = username if username else name
        self.password = password

    def to_dict(self):
        doctor_dict = {
            "doctor_id": self.doctor_id,
            "name": self.name,
            "specialization": self.specialization,
            "department": self.department
        }
        return doctor_dict

    def can_treat(self, disease):
        if disease == self.specialization:
            return True
        else:
            return False

    def diagnose(self, patient_obj):
        print(f"\n---- Dr. {self.name} examining patient {patient_obj.name} ----")
        diagnosis = input("Enter the patient's diagnosis (disease): ").strip()
        patient_obj.disease = diagnosis
        return diagnosis


class department:
    def __init__(self, department_id, name):
        self.department_id = department_id
        self.name = name

    def to_dict(self):
        department_dict = {
            "department_id": self.department_id,
            "name": self.name
        }
        return department_dict


class appointment:
    def __init__(self, patient, doctor, time, status="pending"):
        self.patient = patient
        self.doctor = doctor
        self.time = time
        self.status = status

    def confirm(self):
        if self.status == "cancelled":
            return False, "Appointment is cancelled and cannot be confirmed"
        self.status = "confirmed"
        return True, "Appointment confirmed for patient " + self.patient.name

    def cancel(self):
        self.status = "cancelled"

    def app_dict(self):
        result = {}
        result["patient"] = self.patient.name
        result["doctor"] = self.doctor.name
        result["time"] = self.time
        result["status"] = self.status
        return result


class regular_appointment(appointment):
    def __init__(self, patient, doctor, time, status="pending"):
        super().__init__(patient, doctor, time, status)
        self.duration_minutes = 30


class emergency_appointment(appointment):
    def __init__(self, patient, doctor, time, status="pending"):
        super().__init__(patient, doctor, time, status)
        self.priority = "high"

    def confirm(self):
        if self.status == "cancelled":
            return False, "Emergency appointment is cancelled and cannot be confirmed"

        self.status = "confirmed"
        return True, "Emergency appointment confirmed for patient " + self.patient.name


class Schedule:
    def __init__(self, doctor):
        self.doctor = doctor
        self.appointments = []

    def is_available(self, requested_time):
        for appoint in self.appointments:
            if appoint.time == requested_time and appoint.status != "cancelled":
                return False
        return True

    def book_appointment(self, patient, requested_time, appointment_type="regular"):
        if self.is_available(requested_time) == False:
            return appointment(patient, self.doctor, requested_time, status="rejected")

        if appointment_type == "emergency":
            new_appointment = emergency_appointment(patient, self.doctor, requested_time)
        else:
            new_appointment = regular_appointment(patient, self.doctor, requested_time)
        self.appointments.append(new_appointment)
        return new_appointment

    def cancel_appointment(self, appointment):
        appointment.cancel()

    def get_available_times(self, possible_times):
        available = []
        for time in possible_times:
            if self.is_available(time):
                available.append(time)

        return available


class Auth:
    def __init__(self):
        self.username = "admin"
        self.password = "1234"

    def admin_login(self):
        user = input("Admin username: ")
        pw = input("Admin password: ")

        if user == self.username and pw == self.password:
            print("Admin login successful")
            return True
        else:
            print("Wrong username or password")
            return False

    def doctor_login(self, doctors):
        user = input("Doctor username or Name: ")
        for doctor in doctors:
            if doctor.username == user or doctor.name == user or str(doctor.doctor_id) == user:
                if doctor.password is not None:
                    pw = input("Doctor password: ")
                    if pw != doctor.password:
                        print("Wrong password")
                        return None

                print("Doctor login successful")
                print("Welcome", doctor.name)
                return doctor

        print("Wrong doctor username or name")
        return None


class FileStorage:
    def load_data(self, file_name):
        with open(file_name, "r") as file:
            return json.load(file)

    def save_data(self, file_name, data):
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)

    def export_to_csv(self, json_file, csv_file):
        with open(json_file, "r") as file:
            data = json.load(file)
        with open(csv_file, "w", newline="") as file:
            writer = csv.writer(file)
            if len(data) > 0:
                writer.writerow(data[0].keys())
                for row in data:
                    writer.writerow(row.values())


class MedicalReport:

    REPORTS_FILE = "reports_data.json"
    def __init__(self):
        self.storage = FileStorage()

    def load_all_reports(self):
        if not os.path.exists(self.REPORTS_FILE):
            return []
        try:
            return self.storage.load_data(self.REPORTS_FILE)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_patient_history(self, patient_id):
        all_reports = self.load_all_reports()
        history = []
        for r in all_reports:
            if str(r.get("patient_id")) == str(patient_id):
                history.append(r)
        return history

    def print_history(self, patient_id):
        history = self.get_patient_history(patient_id)
        if not history:
            print("\nNo previous reports found for this patient. This is their first visit.")
            return history

        print("\n========== PREVIOUS VISITS / REPORTS ==========")
        for i, r in enumerate(history, start=1):
            print(f"\n--- Visit #{i} ---")
            print("Date:", r.get("visit_date"))
            print("Diagnosis:", r.get("disease"))
            print("Doctor:", r.get("doctor_name"))
            print("Department:", r.get("department"))
            print("Status:", r.get("appointment_status"))
        print("=================================================")
        return history

    def build_report(self, patient_obj, doctor_obj, appointment_obj):
        report = {
            "patient_id": patient_obj.patient_id,
            "patient_name": patient_obj.name,
            "age": patient_obj.age,
            "gender": patient_obj.gender,
            "blood_type": patient_obj.blood_type,
            "disease": patient_obj.disease,
            "doctor_name": doctor_obj.name,
            "department": doctor_obj.department,
            "appointment_time": appointment_obj.time,
            "appointment_status": appointment_obj.status,
            "visit_date": str(datetime.now().date())
        }
        return report

    def save_report(self, report):
        all_reports = self.load_all_reports()
        all_reports.append(report)
        self.storage.save_data(self.REPORTS_FILE, all_reports)

    def print_report(self, report):
        print("\n==========================================")
        print("             PATIENT MEDICAL REPORT")
        print("==========================================")
        print("Patient Name :", report["patient_name"])
        print("Patient ID   :", report["patient_id"])
        print("Age          :", report["age"])
        print("Gender       :", report["gender"])
        print("Blood Type   :", report["blood_type"])
        print("Diagnosis    :", report["disease"])
        print("Doctor       :", report["doctor_name"])
        print("Department   :", report["department"])
        print("Appointment  :", report["appointment_time"])
        print("Status       :", report["appointment_status"])
        print("Visit Date   :", report["visit_date"])
        print("==========================================")

    def save_report_as_text_file(self, report):
        safe_id = str(report["patient_id"]).replace(" ", "_")
        safe_date = report["visit_date"].replace(":", "-").replace(" ", "_")
        filename = f"report_{safe_id}_{safe_date}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write("==========================================\n")
            f.write("             PATIENT MEDICAL REPORT\n")
            f.write("==========================================\n")
            f.write(f"Patient Name : {report['patient_name']}\n")
            f.write(f"Patient ID   : {report['patient_id']}\n")
            f.write(f"Age          : {report['age']}\n")
            f.write(f"Gender       : {report['gender']}\n")
            f.write(f"Blood Type   : {report['blood_type']}\n")
            f.write(f"Diagnosis    : {report['disease']}\n")
            f.write(f"Doctor       : {report['doctor_name']}\n")
            f.write(f"Department   : {report['department']}\n")
            f.write(f"Appointment  : {report['appointment_time']}\n")
            f.write(f"Status       : {report['appointment_status']}\n")
            f.write(f"Visit Date   : {report['visit_date']}\n")
            f.write("==========================================\n")

        return filename


def load_doctors_from_csv(csv_file):
    doctors_list = []
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            header = next(reader, None)
            for row in reader:
                if row:
                    d_id = row[0].strip()
                    name = row[1].strip()
                    spec = row[2].strip()
                    dept = row[3].strip()
                    doctors_list.append(doctor(d_id, name, spec, dept))
    except FileNotFoundError:
        pass
    return doctors_list


def find_existing_patient(patient_id):
    storage = FileStorage()
    try:
        patients = storage.load_data("patients_data.json")
    except (FileNotFoundError, json.JSONDecodeError):
        patients = []

    for p in patients:
        if str(p.get("patient_id")) == str(patient_id):
            return p
    return None


def main():
    print("=" * 50)
    print("       HOSPITAL BOOKING SYSTEM")
    print("=" * 50)

    all_doctors = load_doctors_from_csv("doctors_data.csv")

    if not all_doctors:
        print("No doctors found.")
        return

    print("\n========== PATIENT REGISTRATION ==========")

    patient_id = input("Enter patient ID: ")
    report_manager = MedicalReport()
    existing_record = find_existing_patient(patient_id)
    report_manager.print_history(patient_id)

    if existing_record:
        print("\nWelcome back! We already have your details on file.")
        name = existing_record["name"]
        age = existing_record["age"]
        gender = existing_record["gender"]
        blood_type = existing_record["blood_type"]
    else:
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))
        gender = input("Enter your gender: ")
        blood_type = input("Enter your blood type: ")

    new_patient = patient(patient_id, name, age, gender, blood_type, disease=None)

    print("\nPatient registered successfully!")

    print("\n========== AVAILABLE DOCTORS ==========")
    for i in range(len(all_doctors)):
        print(
            f"{i + 1}. "
            f"{all_doctors[i].name} - "
            f"{all_doctors[i].specialization} ({all_doctors[i].department})"
        )
    doctor_choice = int(input("Choose the doctor who will examine the patient: "))
    selected_doctor = all_doctors[doctor_choice - 1]
    print("\nSelected doctor:", selected_doctor.name)

    selected_doctor.diagnose(new_patient)

    if not selected_doctor.can_treat(new_patient.disease):
        print(
            f"\n⚠ Warning: Dr. {selected_doctor.name}'s specialization is "
            f"'{selected_doctor.specialization}', which does not match the diagnosis "
            f"'{new_patient.disease}'. Consider referring the patient to a suitable doctor."
        )

    schedule = Schedule(selected_doctor)
    possible_times = [
        "09:00 AM",
        "10:00 AM",
        "11:00 AM",
        "12:00 PM",
        "01:00 PM"
    ]
    available_times = schedule.get_available_times(
        possible_times
    )

    print("\n========== AVAILABLE TIMES ==========")

    for i in range(len(available_times)):
        print(
            f"{i + 1}. {available_times[i]}"
        )

    time_choice = int(input("Choose a time: "))
    selected_time = available_times[time_choice - 1]

    print("\n========== APPOINTMENT TYPE ==========")
    print("1. Regular")
    print("2. Emergency")

    appointment_choice = input(
        "Choose appointment type: "
    )

    if appointment_choice == "2":
        appointment_type = "emergency"
    else:
        appointment_type = "regular"

    booked_appointment = schedule.book_appointment(
        new_patient,
        selected_time,
        appointment_type
    )

    if booked_appointment.status == "rejected":
        print("\nAppointment was rejected.")
        return

    success, message = booked_appointment.confirm()
    print("\n" + message)

    if not success:
        return

    storage = FileStorage()
    patients = []

    try:
        patients = storage.load_data(
            "patients_data.json"
        )
    except (FileNotFoundError, json.JSONDecodeError):
        patients = []
    patients = [p for p in patients if str(p.get("patient_id")) != str(patient_id)]
    patients.append(new_patient.to_dict())

    storage.save_data(
        "patients_data.json",
        patients
    )

    appointments = []
    try:
        appointments = storage.load_data(
            "appointments_data.json"
        )
    except (FileNotFoundError, json.JSONDecodeError):
        appointments = []

    appointments.append(booked_appointment.app_dict())

    storage.save_data("appointments_data.json", appointments)
    report = report_manager.build_report(new_patient, selected_doctor, booked_appointment)
    report_manager.save_report(report)
    report_manager.print_report(report)
    report_filename = report_manager.save_report_as_text_file(report)

    print(f"\nReport saved to file: {report_filename}")
    print("Thank you for using Hospital Booking System!")
    print("Goodbye!")


if __name__ == "__main__":
    main()