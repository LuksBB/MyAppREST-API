from app import db
from sqlalchemy.orm import relationship

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    lastname = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    sex = db.Column(db.String(10), nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Integer, nullable=True)

    medicines = relationship("User_Medicine", back_populates="user", lazy="dynamic", cascade="all, delete")

    def __init__(self, username, name, lastname, public_id):
        self.username=username
        self.name=name
        self.lastname=lastname
        self.public_id=public_id

class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.String(80), unique=False, nullable=True) #czy da sie latwiej zmienic typ?

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False) #czy to nie powielenie danych?
    company = relationship("Company", back_populates="medicines")

    users = relationship("User_Medicine", back_populates="medicine", lazy="dynamic", cascade="all, delete")

    def __init__(self, name, company_id):
        self.name=name
        self.company_id=company_id

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(150), unique=False, nullable=False)
    phone_number = db.Column(db.Integer, unique=True, nullable=True)
    email = db.Column(db.String, unique=True, nullable=True)

    medicines = relationship("Medicine", back_populates="company", lazy="dynamic", cascade="all, delete")

    def __init__(self, name, address):
        self.name=name
        self.address=address

class User_Medicine(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.id'), primary_key=True)
    dosage_quantity = db.Column(db.Integer, nullable=False)
    dosage_units = db.Column(db.String(80), nullable=False)
    frequency_quantity = db.Column(db.Integer, nullable=False)
    frequency_units = db.Column(db.String(80), nullable=False)

    user = relationship("User", back_populates="medicines")
    medicine = relationship("Medicine", back_populates="users")