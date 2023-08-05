# from mongoengine import Document, StringField, IntField, EnumField, DateField, DateTimeField, ReferenceField, ListField, connect, DictField
# from datetime import datetime, timedelta
import json
from flask_pymongo import PyMongo
# import jwt
import os
# import requests
# from bson import json_util, ObjectId
from flask import Flask, jsonify, request
# from flask_bcrypt import Bcrypt
# from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()
port=os.getenv('PORT') or 8000
app = Flask(__name__)
# CORS(app)
# bcrypt = Bcrypt(app)
mongoUrl = os.getenv("MONGO_URI")
secret_key = os.getenv("SECRET_KEY")
# Set up MongoDB connection using flask_pymongo
app.config["MONGO_URI"] = mongoUrl
db = PyMongo(app).db

# bcrypt = Bcrypt(app)

# Define default connection
# connect('vacationrental', host=mongoUrl)

# Define the schema for the Host collection using mongoengine


# class Host(Document):
#     name = StringField(required=True)
#     host_status = StringField(
#         choices=["Active", "Inactive", "Pending"], required=True)
#     location = StringField()
#     email = StringField(required=True)
#     password = StringField(required=True)
#     about = StringField()
#     hosting_since = DateTimeField(default=datetime.utcnow, required=True)


# class Property(Document):
#     host_id = IntField(required=True)
#     property_name = StringField(required=True)
#     property_type = StringField(
#         choices=["Apartment", "House", "Unique Homes"], default="House")
#     description = StringField()
#     address = StringField(max_length=200)
#     city = StringField(max_length=100)
#     state = StringField(max_length=100)
#     zip_code = StringField(max_length=20)
#     image_url = StringField()
#     sub_img_urls = ListField(StringField())
#     price = IntField(required=True)

    # Reference field for the relationship with the 'Host' collection
    # host_ref = ReferenceField("Host", reverse_delete_rule=2)  # 2: CASCADE


# class Guest(Document):
#     name = StringField(required=True, max_length=100)
#     gender = StringField(choices=["Male", "Female", "Other"])
#     date_of_birth = DateField()
#     bio = StringField()


# class Booking(Document):
#     property_id = IntField(required=True)
#     guest_id = IntField(required=True)
#     check_in = DateField(required=True)
#     check_out = DateField(required=True)
#     booking_date = DateTimeField(default=datetime.utcnow)

#     # Reference fields for the relationships with other collections
#     property_ref = ReferenceField(
#         "Property", reverse_delete_rule=2)  # 2: CASCADE
#     guest_ref = ReferenceField("Guest", reverse_delete_rule=2)


@app.route('/', methods=["GET"])
def index():
    # url = "https://hotels4.p.rapidapi.com/v2/get-meta-data"
    # headers = {
    #     "X-RapidAPI-Key": "75d3790496msha75da2eb49c3cb2p11cefcjsnf88b8e0f67cb",
    #     "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    # }
    # response = requests.get(url, headers=headers)
    return jsonify({"success": "this is the home page , running successfully"})


# @app.route('/host/register', methods=['POST'])
# def create_host():
#     try:
#         data = request.json
#         name = data.get('name')
#         host_status = data.get('host_status')
#         location = data.get('location')
#         about = data.get('about')
#         hosting_since = data.get('hosting_since')
#         password = data.get('password')
#         email = data.get('email')
#         bcrypt_pass = bcrypt.generate_password_hash(
#             password, rounds=5).decode("UTF-8")

#         user = db.host.find_one({"email": email})
#         if user:
#             return jsonify({"message": "you are already registered"}), 401

#         # Insert host data into the MongoDB collection
#         db.host.insert_one({
#             "name":name,
#             "host_status":host_status,
#             "location":location,
#             "email":email,
#             "password":bcrypt_pass,
#             "about":about,
#             "hosting_since":hosting_since
#         }
#         )
#         # setHost.save()
#         return jsonify({"message": "Host created successfully"}), 201
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route('/host/login', methods=['POST'])
# def login_host():
#     try:
#         data = request.json
#         email = data.get('email')
#         password = data.get('password')

#         # Retrieve the user data from the MongoDB collection based on the provided email
#         user = db.host.find_one({"email": email})
#         if user and bcrypt.check_password_hash(user['password'], password):
#             # Password is correct, user is authenticated
#             # Generate JWT access token with expiry time (e.g., 1 hour)
#             access_token_payload = {
#                 "email": email,
#                 "exp": datetime.utcnow() + timedelta(hours=1)
#             }
#             access_token = jwt.encode(
#                 access_token_payload, secret_key, algorithm="HS256")

#             return jsonify({"access_token": access_token, "message": "Login successful"}), 200

#         else:
#             # Invalid credentials
#             return jsonify({"message": "Invalid email or password"}), 401
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route("/host/all", methods=["GET"])
# def host_all():
#     allHosts = db.host.find()

#     return json.loads(json_util.dumps(allHosts))


# @app.route('/host/<host_id>', methods=['GET', 'PUT', 'DELETE'])
# def manage_host(host_id):
#     if request.method == 'GET':
#         try:
#             # Retrieve the host data from the MongoDB collection based on the provided host_id
#             host = db.host.find_one({"_id": ObjectId(host_id)})
#             print(host)
#             if host:
#                 host["_id"] = str(host["_id"])
#                 return jsonify(host)
#                 # return jsonify({
#                 #     "id": host['_id'],
#                 #     "name": host['name'],
#                 #     "host_status": host['host_status'],
#                 #     "location": host['location'],
#                 #     "email": host['email'],
#                 #     "about": host['about'],
#                 #     "hosting_since": host['hosting_since'].strftime("%m-%d-%Y")
#                 # })
#             return jsonify({"message": "Host not found"}), 404
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500

#     elif request.method == 'PUT':
#         try:
#             data = request.json
#             name = data.get('name')
#             host_status = data.get('host_status')
#             location = data.get('location')
#             about = data.get('about')
#             # hosting_since = data.get('hosting_since')

#             # Update the host data in the MongoDB collection based on the provided host_id
#             db.host.update_one({"_id": ObjectId(host_id)}, {
#                 "$set": {
#                     "name": name,
#                     "host_status": host_status,
#                     "location": location,
#                     "about": about,
#                     # "hosting_since": datetime.strptime(hosting_since, "%m-%d-%Y")
#                 }
#             })

#             return jsonify({"message": "Host updated successfully"}), 200
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500

#     elif request.method == 'DELETE':
#         try:
#             # Delete the host data from the MongoDB collection based on the provided host_id
#             db.host.delete_one({"_id": ObjectId(host_id)})

#             return jsonify({"message": "Host deleted successfully"}), 200
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500


# @app.route('/property', methods=['POST'])
# def create_property():
#     try:
#         data = request.json
#         host_id = int(data.get('host_id'))
#         property_name = data.get('property_name')
#         property_type = data.get('property_type')
#         description = data.get('description')
#         address = data.get('address')
#         city = data.get('city')
#         state = data.get('state')
#         zip_code = data.get('zip_code')
#         image_url = data.get('image_url')
#         sub_img_urls = data.get('sub_img_urls')
#         price = int(data.get('price'))

#         # Create a Property object
#         setProperty = Property(
#             host_id=host_id,
#             property_name=property_name,
#             property_type=property_type,
#             description=description,
#             address=address,
#             city=city,
#             state=state,
#             zip_code=zip_code,
#             image_url=image_url,
#             sub_img_urls=sub_img_urls,
#             price=price
#         )

#         setProperty.save()

#         return jsonify({"message": "Property created successfully"}), 201
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route('/property/<property_id>', methods=['GET', 'PUT', 'DELETE'])
# def manage_property(property_id):
#     if request.method == 'GET':
#         try:
#             property_data = db.property.find_one(
#                 {"_id": ObjectId(property_id)})
#             if property_data:
#                 # Convert ObjectId to str for JSON serialization
#                 property_data['_id'] = str(property_data['_id'])

#                 return jsonify(property_data)
#             return jsonify({"message": "Property not found"}), 404
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500

#     elif request.method == 'PUT':
#         try:
#             data = request.json
#             property_name = data.get('property_name')
#             property_type = data.get('property_type')
#             description = data.get('description')
#             address = data.get('address')
#             city = data.get('city')
#             state = data.get('state')
#             zip_code = data.get('zip_code')
#             image_url = data.get('image_url')
#             sub_img_urls = data.get('sub_img_urls')

#             # Convert sub_img_urls list to a JSON serializable format
#             sub_img_urls = [str(url) for url in sub_img_urls]

#             # Update property data in the MongoDB collection
#             db.property.update_one({"id": property_id}, {
#                 "$set": {
#                     "property_name": property_name,
#                     "property_type": property_type,
#                     "description": description,
#                     "address": address,
#                     "city": city,
#                     "state": state,
#                     "zip_code": zip_code,
#                     "image_url": image_url,
#                     "sub_img_urls": sub_img_urls
#                 }
#             })

#             return jsonify({"message": "Property updated successfully"}), 200
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500

#     elif request.method == 'DELETE':
#         try:
#             # Delete property from the MongoDB collection
#             db.property.delete_one({"id": property_id})

#             return jsonify({"message": "Property deleted successfully"}), 200
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=port)
