from flask import Blueprint, request

from nursing_knowledge_ia_back.controllers.admin.admin import AdminController
from nursing_knowledge_ia_back.controllers.doctor.doctor import DoctorController
from nursing_knowledge_ia_back.repositories.admin.admin import AdminRepository
from nursing_knowledge_ia_back.repositories.doctor.doctor import DoctorRepository
from nursing_knowledge_ia_back.services.admin.admin import AdminService
from nursing_knowledge_ia_back.services.doctor.doctor import DoctorService


class ApiRoutes:
    def __init__(self, client):
        self.client = client
        admin_repository = AdminRepository(self.client)
        admin_service = AdminService(admin_repository)
        self.admin_controller = AdminController(admin_service)
        doctor_repository = DoctorRepository(self.client)
        doctor_service = DoctorService(doctor_repository)
        self.doctor_controller = DoctorController(doctor_service)
        self.blueprint = Blueprint("admins", __name__)

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

    def register_routes(self, app):
        app.register_blueprint(self.blueprint)

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
