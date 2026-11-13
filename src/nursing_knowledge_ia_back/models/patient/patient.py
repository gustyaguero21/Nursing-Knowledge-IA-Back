class Patient:

    def __init__(self, name, lastname, pid,email, password, createdAt, active, age, sex, currentDiagnosis, dateOfEntry):
        self.name = name
        self.lastname = lastname
        self.pid=pid
        self.email = email
        self.password = password
        self.createdAt = createdAt
        self.active = active
        self.age = age
        self.sex = sex
        self.currentDiagnosis = currentDiagnosis
        self.dateOfEntry = dateOfEntry
