from app import app, db
from flask import request, jsonify
from models import *
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import auth

cred = credentials.Certificate(f"./Secret/myappproject-22a33-firebase-adminsdk-3psao-157a154318.json")
firebase_admin.initialize_app(cred)

@app.route('/', methods=['GET', 'POST'])
def home():
    return jsonify(message="Welcome to MyApp ! How can I help you?")

@app.route("/register/user", methods=['POST'])
def create_user():
    data = request.get_json()
    user = auth.create_user(email=data['email'], password=data['password'])
    new_user = User(username=data['username'], name=data['name'], lastname=data['lastname'], public_id=user.uid)   
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="Created user with id: " + str(new_user.id)), 200

@app.route("/register/medicine", methods=['POST'])
def create_medicine():
    data = request.get_json()
    new_medicine = Medicine(data['name'], data['company_id'])   
    db.session.add(new_medicine)
    db.session.commit()
    return jsonify(message="Created medicine with id: " + str(new_medicine.id)), 200

@app.route("/register/company", methods=['POST'])
def create_company():
    data = request.get_json()
    new_company = Company(data['name'], data['address'])  
    db.session.add(new_company)
    db.session.commit()
    return jsonify(message="Created company with id: " + str(new_company.id)), 200

#to chyba bedzie do usuniecia
@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    user_data = request.headers['user_data']
    return data['login'] + ' ' + data['password'] + ' ' + user_data, 200 #?

@app.route("/users/<user_id>", methods=['DELETE', 'PUT'])
def update_user(user_id):
    if request.method=="DELETE":
        user = User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        return jsonify(message="User deleted"), 201
    elif request.method=="PUT":
        data = request.get_json()
        user = User.query.filter_by(id=user_id).first()
        user.sex = data['sex']
        user.birthday = data['birthday']
        user.height = data['height']
        user.weight = data['weight']
        db.session.commit()
        return jsonify(message="Data updated :)"), 201

@app.route("/medicines/<medicine_id>", methods=['DELETE', 'PUT'])
def update_medicine(medicine_id):
    if request.method=="DELETE":
        medicine = Medicine.query.filter_by(id=medicine_id).first()
        db.session.delete(medicine)
        db.session.commit()
        return jsonify(message="Medicine deleted"), 201
    elif request.method=="PUT":
        data = request.get_json()
        medicine = Medicine.query.filter_by(id=medicine_id).first()
        medicine.price = data['price']
        db.session.commit()
        return jsonify(message="Data updated :)"), 201

@app.route("/companies/<company_id>", methods=['DELETE', 'PUT'])
def update_company(company_id):
    if request.method=="DELETE":
        #company_id = request.headers['company_id']
        company = Company.query.filter_by(id=company_id).first()
        db.session.delete(company)
        db.session.commit()
        return jsonify(message="Company deleted"), 201
    elif request.method=="PUT":
        data = request.get_json()
        company = Company.query.filter_by(id=company_id).first()
        company.phone_number = data['phone_number']
        company.email = data['email']
        db.session.commit()
        return jsonify(message="Data updated :)"), 201

@app.route("/users/<user_id>", methods=['GET'])
def get_user(user_id):
    #user_id = request.headers['user_id']
    user = User.query.filter_by(id=user_id).first()
    return jsonify(name=user.name, lastname=user.lastname)

@app.route("/medicines/<medicine_id>", methods=['GET'])
def get_medicine(medicine_id):
    medicine = Medicine.query.filter_by(id=medicine_id).first()
    return jsonify(name=medicine.name, company=medicine.company.name)  

@app.route("/companies/<company_id>", methods=['GET'])
def get_company(company_id):
    company = Company.query.filter_by(id=company_id).first()
    return jsonify(name=company.name, address=company.address)

@app.route("/users", methods=['GET'])
def get_users():
    users_entries = User.query.filter_by().all()
    users = []
    for users_entry in users_entries:
        user = {}
        user['name'] = users_entry.name
        user['lastname'] = users_entry.lastname
        user['username'] = users_entry.username
        users.append(user)
    return jsonify(users=users), 200

@app.route("/users/<user_id>/medicines", methods=['POST', 'DELETE'])
def update_user_medicine(user_id):
    if request.method == "POST":
        data = request.get_json()
        user = User.query.filter_by(id=user_id).first()
        medicine = Medicine.query.filter_by(id=data['medicine_id']).first()
        new_user_medicine = User_Medicine(user_id=user.id, medicine_id=medicine.id, dosage_quantity=data['dosage_quantity'], dosage_units=data['dosage_units'], frequency_quantity=data['frequency_quantity'], frequency_units=data['frequency_units'])
        db.session.add(new_user_medicine)
        db.session.commit()
        return jsonify(message=user.name + ", you have succesfully added " + medicine.name + " to your medicines"), 200
    elif request.method == "DELETE":
        data = request.get_json()
        user = User.query.filter_by(id=user_id).first()
        medicine = Medicine.query.filter_by(id=data['medicine_id']).first()
        user_med = User_Medicine.query.filter_by(user_id=user.id, medicine_id=medicine.id).first()  
        db.session.delete(user_med)
        db.session.commit()
        return jsonify(message=user.name + ", you have succesfully removed " + medicine.name + " from your medicines"), 201