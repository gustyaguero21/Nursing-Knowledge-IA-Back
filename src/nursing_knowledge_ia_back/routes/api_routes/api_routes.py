from flask import Blueprint, request

from nursing_knowledge_ia_back.controllers.admin.admin import AdminController
from nursing_knowledge_ia_back.controllers.doctor.doctor import DoctorController
from nursing_knowledge_ia_back.controllers.login.login import LoginController
from nursing_knowledge_ia_back.controllers.nurse.nurse import NurseController
from nursing_knowledge_ia_back.controllers.patient.patient import PatientController
from nursing_knowledge_ia_back.repositories.admin.admin import AdminRepository
from nursing_knowledge_ia_back.repositories.doctor.doctor import DoctorRepository
from nursing_knowledge_ia_back.repositories.login.login import LoginRepository
from nursing_knowledge_ia_back.repositories.nurse.nurse import NurseRepository
from nursing_knowledge_ia_back.repositories.patient.patient import PatientRepository
from nursing_knowledge_ia_back.services.admin.admin import AdminService
from nursing_knowledge_ia_back.services.doctor.doctor import DoctorService
from nursing_knowledge_ia_back.services.login.login import LoginService
from nursing_knowledge_ia_back.services.nurse.nurse import NurseService
from nursing_knowledge_ia_back.services.patient.patient import PatientService


class ApiRoutes:
    def __init__(self, client):
        self.client = client
        admin_repository = AdminRepository(self.client)
        admin_service = AdminService(admin_repository)
        self.admin_controller = AdminController(admin_service)
        doctor_repository = DoctorRepository(self.client)
        doctor_service = DoctorService(doctor_repository)
        self.doctor_controller = DoctorController(doctor_service)
        nurse_repository = NurseRepository(self.client)
        nurse_service = NurseService(nurse_repository)
        self.nurse_controller = NurseController(nurse_service)
        patient_repository = PatientRepository(self.client)
        patient_service = PatientService(patient_repository)
        self.patient_controller = PatientController(patient_service)
        login_repository = LoginRepository(self.client)
        login_service = LoginService(login_repository)
        self.login_controller = LoginController(login_service)
        self.blueprint = Blueprint("admins", __name__)

        self.blueprint.add_url_rule(
            "/login", "login", self.login, methods=["POST"]
        )
        self.blueprint.add_url_rule(
            "/admins", "create_admin", self.create_admin, methods=["POST"]
        )
        self.blueprint.add_url_rule(
            "/admins/<string:email>",
            "update_admin",
            self.update_admin,
            methods=["PUT"],
        )
        self.blueprint.add_url_rule(
            "/admins/<string:email>",
            "delete_admin",
            self.delete_admin,
            methods=["DELETE"],
        )
        self.blueprint.add_url_rule(
            "/doctors", "create_doctor", self.create_doctor, methods=["POST"]
        )
        self.blueprint.add_url_rule(
            "/doctors", "get_doctors", self.get_doctors, methods=["GET"]
        )
        self.blueprint.add_url_rule(
            "/doctors/<string:register>",
            "get_doctor_by_register",
            self.get_doctor_by_register,
            methods=["GET"],
        )
        self.blueprint.add_url_rule(
            "/doctors/<string:register>",
            "update_doctor",
            self.update_doctor,
            methods=["PUT"],
        )
        self.blueprint.add_url_rule(
            "/doctors/<string:register>",
            "delete_doctor",
            self.delete_doctor,
            methods=["DELETE"],
        )
        self.blueprint.add_url_rule(
            "/nurses", "create_nurse", self.create_nurse, methods=["POST"]
        )
        self.blueprint.add_url_rule(
            "/nurses", "get_nurses", self.get_nurses, methods=["GET"]
        )
        self.blueprint.add_url_rule(
            "/nurses/<string:file>",
            "get_nurse_by_file",
            self.get_nurse_by_file,
            methods=["GET"],
        )
        self.blueprint.add_url_rule(
            "/nurses/<string:file>",
            "update_nurse",
            self.update_nurse,
            methods=["PUT"],
        )
        self.blueprint.add_url_rule(
            "/nurses/<string:file>",
            "delete_nurse",
            self.delete_nurse,
            methods=["DELETE"],
        )
        self.blueprint.add_url_rule(
            "/patients", "create_patient", self.create_patient, methods=["POST"]
        )
        self.blueprint.add_url_rule(
            "/patients", "get_patients", self.get_patients, methods=["GET"]
        )
        self.blueprint.add_url_rule(
            "/patients/<string:pid>",
            "get_patient_by_pid",
            self.get_patient_by_pid,
            methods=["GET"],
        )
        self.blueprint.add_url_rule(
            "/patients/<string:pid>",
            "update_patient",
            self.update_patient,
            methods=["PUT"],
        )
        self.blueprint.add_url_rule(
            "/patients/<string:pid>",
            "delete_patient",
            self.delete_patient,
            methods=["DELETE"],
        )

    def register_routes(self, app):
        app.register_blueprint(self.blueprint)

    def login(self):
        return self.login_controller.login(request.get_json(silent=True))

    def create_admin(self):
        return self.admin_controller.create_admin(request.get_json(silent=True))

    def update_admin(self, email):
        # El repositorio identifica al administrador por su correo electrónico.
        return self.admin_controller.update_admin(email, request.get_json(silent=True))

    def delete_admin(self, email):
        return self.admin_controller.delete_admin(email)

    def create_doctor(self):
        return self.doctor_controller.create_doctor(request.get_json(silent=True))

    def get_doctors(self):
        return self.doctor_controller.get_doctors()

    def get_doctor_by_register(self, register):
        return self.doctor_controller.get_doctor_by_register(register)

    def update_doctor(self, register):
        return self.doctor_controller.update_doctor(
            register, request.get_json(silent=True)
        )

    def delete_doctor(self, register):
        return self.doctor_controller.delete_doctor(register)

    def create_nurse(self):
        return self.nurse_controller.create_nurse(request.get_json(silent=True))

    def get_nurses(self):
        return self.nurse_controller.get_nurses()

    def get_nurse_by_file(self, file):
        return self.nurse_controller.get_nurse_by_file(file)

    def update_nurse(self, file):
        return self.nurse_controller.update_nurse(
            file, request.get_json(silent=True)
        )

    def delete_nurse(self, file):
        return self.nurse_controller.delete_nurse(file)

    def create_patient(self):
        return self.patient_controller.create_patient(request.get_json(silent=True))

    def get_patients(self):
        return self.patient_controller.get_patients()

    def get_patient_by_pid(self, pid):
        return self.patient_controller.get_patient_by_pid(pid)

    def update_patient(self, pid):
        return self.patient_controller.update_patient(
            pid, request.get_json(silent=True)
        )

    def delete_patient(self, pid):
        return self.patient_controller.delete_patient(pid)
