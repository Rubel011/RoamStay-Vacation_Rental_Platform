from flask import Flask, jsonify, request
from dotenv import load_dotenv
from flask_mysqldb import MySQL
import json
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import requests
import os
load_dotenv()
app = Flask(__name__)
CORS(app,resources={r"/*":{"origin": "*"}})
bcrypt=Bcrypt(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.getenv("mysql_password")
app.config['MYSQL_DB'] = 'vacationRental'

# app.config['MYSQL_HOST'] = os.getenv('HOST')
# app.config['MYSQL_USER'] = os.getenv('USERNAME')
# app.config['MYSQL_PASSWORD'] = os.getenv('PASSWORD')
# app.config['MYSQL_DB'] = os.getenv('DATABASE')
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# SSL configuration for secure connections
# app.config['MYSQL_SSL_MODE'] = 'VERIFY_IDENTITY'
# app.config['MYSQL_SSL_CA'] = '/path/to/your/ca-certificates.crt'  # Update this to the correct path


mysql = MySQL(app)
# api = Api(app)


# Create the Host table if it doesn't exist
with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Host (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            host_status varchar(50) DEFAULT 'Active',
            location VARCHAR(200),
            email varchar(100) not null,
            password varchar(200) not null,
            about TEXT,
            hosting_since TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
    """)
    cur.execute("""
       CREATE TABLE IF NOT EXISTS Property (
            id INT AUTO_INCREMENT PRIMARY KEY,
            host_id INT NOT NULL,
            property_name VARCHAR(100) NOT NULL,
            property_type ENUM("Apartment", "House", "Unique Homes") NOT NULL DEFAULT "House",
            description TEXT,
            address VARCHAR(200),
            city VARCHAR(100),
            state VARCHAR(100),
            zip_code VARCHAR(20),
            image_url VARCHAR(200), 
            sub_img_urls JSON, 
            CONSTRAINT fk_host
                FOREIGN KEY (host_id)
                REFERENCES Host (id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        )
    """)
    cur.execute("""
            CREATE TABLE IF NOT EXISTS Guest (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                gender ENUM("Male", "Female", "Other"),
                date_of_birth DATE,
                bio TEXT
            )
    """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS Booking (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    property_id INT NOT NULL,
                    guest_id INT NOT NULL,
                    check_in DATE NOT NULL,
                    check_out DATE NOT NULL,
                    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT fk_property
                        FOREIGN KEY (property_id)
                        REFERENCES Property (id)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE,
                    CONSTRAINT fk_guest
                        FOREIGN KEY (guest_id)
                        REFERENCES Guest (id)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE
            )
    """)
    mysql.connection.commit()
    cur.close()


@app.route('/', methods=["GET"])
def index():
    url = "https://hotels4.p.rapidapi.com/v2/get-meta-data"
    headers = {
        "X-RapidAPI-Key": "75d3790496msha75da2eb49c3cb2p11cefcjsnf88b8e0f67cb",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    # print(response.json())
    return response.json()


@app.route('/host/register', methods=['POST'])
def create_host():
    try:
        data = request.json
        name = data.get('name')
        host_status = data.get('host_status')
        location = data.get('location')
        about = data.get('about')
        hosting_since = data.get('hosting_since')
        password = data.get('password')
        email = data.get('email')
        bcrypt_pass = bcrypt.generate_password_hash(password, rounds=5).decode("UTF-8")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Host (name, host_status, location,email,password ,about, hosting_since) "
                    "VALUES (%s, %s, %s, %s, %s, %s,%s)",
                    (name, host_status, location,email,bcrypt_pass, about, hosting_since))
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Host created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/host/login', methods=['POST'])
def login_host():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Retrieve the user data from the database based on the provided email
        # Your database code here...
        cur = mysql.connection.cursor()
        cur.execute("SELECT email, password FROM Host WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.check_password_hash(user['password'], password):
            # Password is correct, user is authenticated
            return jsonify({"message": "Login successful"}), 200
        else:
            # Invalid credentials
            return jsonify({"message": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/host/<int:host_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_host(host_id):
    if request.method == 'GET':
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM Host WHERE id = %s", (host_id,))
            host = cur.fetchone()
            cur.close()

            print(host)
            # if host:
            #     return jsonify({
            #         "id": host[0],
            #         "name": host[1],
            #         "host_status": bool(host[2]),
            #         "location": host[3],
            #         "property_type": host[4],
            #         "about": host[5],
            #         "hosting_since": host[6]
            #     })
            return jsonify({"message": "Host not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == 'PUT':
        try:
            data = request.json
            name = data.get('name')
            host_status = bool(data.get('host_status'))
            location = data.get('location')
            property_type = data.get('property_type')
            about = data.get('about')
            hosting_since = data.get('hosting_since')

            cur = mysql.connection.cursor()
            cur.execute("UPDATE Host SET name=%s, host_status=%s, location=%s, property_type=%s, about=%s, hosting_since=%s WHERE id=%s",
                        (name, host_status, location, property_type, about, hosting_since, host_id))
            mysql.connection.commit()
            cur.close()

            return jsonify({"message": "Host updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == 'DELETE':
        try:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM Host WHERE id = %s", (host_id,))
            mysql.connection.commit()
            cur.close()

            return jsonify({"message": "Host deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route('/property', methods=['POST'])
def create_property():
    try:
        data = request.json
        host_id = data.get('host_id')
        property_name = data.get('property_name')
        property_type = data.get('property_type')
        description = data.get('description')
        address = data.get('address')
        city = data.get('city')
        state = data.get('state')
        zip_code = data.get('zip_code')
        image_url = data.get('image_url')
        sub_img_urls = data.get('sub_img_urls')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Property (host_id, property_name, property_type, description, address, city, state, zip_code, image_url, sub_img_urls) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (host_id, property_name, property_type, description, address, city, state, zip_code, image_url, json.dumps(sub_img_urls)))
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Property created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/property/<int:property_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_property(property_id):
    if request.method == 'GET':
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM Property WHERE id = %s", (property_id,))
            property_data = cur.fetchone()
            cur.close()
            if property_data:
                return jsonify({
                    "id": property_data[0],
                    "host_id": property_data[1],
                    "property_name": property_data[2],
                    "property_type": property_data[3],
                    "description": property_data[4],
                    "address": property_data[5],
                    "city": property_data[6],
                    "state": property_data[7],
                    "zip_code": property_data[8],
                    "image_url": property_data[9],
                    "sub_img_urls": json.loads(property_data[10])
                })
            return jsonify({"message": "Property not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == 'PUT':
        try:
            data = request.json
            property_name = data.get('property_name')
            property_type = data.get('property_type')
            description = data.get('description')
            address = data.get('address')
            city = data.get('city')
            state = data.get('state')
            zip_code = data.get('zip_code')
            image_url = data.get('image_url')
            sub_img_urls = data.get('sub_img_urls')

            cur = mysql.connection.cursor()
            cur.execute("UPDATE Property SET property_name=%s, property_type=%s, description=%s, address=%s, city=%s, state=%s, zip_code=%s, image_url=%s, sub_img_urls=%s WHERE id=%s",
                        (property_name, property_type, description, address, city, state, zip_code, image_url, json.dumps(sub_img_urls), property_id))
            mysql.connection.commit()
            cur.close()

            return jsonify({"message": "Property updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == 'DELETE':
        try:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM Property WHERE id = %s", (property_id,))
            mysql.connection.commit()
            cur.close()

            return jsonify({"message": "Property deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route('/booking', methods=['POST'])
def create_booking():
    try:
        data = request.json
        property_id = data.get('property_id')
        guest_id = data.get('guest_id')
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        # Add more booking-related fields as per your requirements

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Booking (property_id, guest_id, check_in, check_out) "
                    "VALUES (%s, %s, %s, %s)",
                    (property_id, guest_id, check_in, check_out))
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Booking created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/booking/<int:booking_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_booking(booking_id):
    try:
        if request.method == 'GET':
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM Booking WHERE id = %s", (booking_id,))
            booking = cur.fetchone()
            cur.close()
            if booking:
                return jsonify({
                    "id": booking[0],
                    "property_id": booking[1],
                    "guest_id": booking[2],
                    "check_in": booking[3].isoformat(),  # Convert date to ISO format for JSON serialization
                    "check_out": booking[4].isoformat()  # Convert date to ISO format for JSON serialization
                    # Add more booking-related fields as per your requirements
                })
            return jsonify({"message": "Booking not found"}), 404

        elif request.method == 'PUT':
            data = request.json
            property_id = data.get('property_id')
            guest_id = data.get('guest_id')
            check_in = data.get('check_in')
            check_out = data.get('check_out')
            # Update more booking-related fields as per your requirements

            cur = mysql.connection.cursor()
            cur.execute("UPDATE Booking SET property_id=%s, guest_id=%s, check_in=%s, check_out=%s WHERE id=%s",
                        (property_id, guest_id, check_in, check_out, booking_id))
            mysql.connection.commit()
            cur.close()

            return jsonify({"message": "Booking updated successfully"}), 200

        elif request.method == 'DELETE':
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM Booking WHERE id = %s", (booking_id,))
            mysql.connection.commit()
            cur.close()

            return jsonify({"message": "Booking deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/guest', methods=['POST'])
def create_guest():
    try:
        data = request.json
        name = data.get('name')
        gender = data.get('gender')
        date_of_birth = data.get('date_of_birth')
        bio = data.get('bio')
        # Add more guest-related fields as per your requirements

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Guest (name, gender, date_of_birth, bio) "
                    "VALUES (%s, %s, %s, %s)",
                    (name, gender, date_of_birth, bio))
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Guest created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/guest/<int:guest_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_guest(guest_id):
    try:
        if request.method == 'GET':
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM Guest WHERE id = %s", (guest_id,))
            guest = cur.fetchone()
            cur.close()
            if guest:
                return jsonify({
                    "id": guest[0],
                    "name": guest[1],
                    "gender": guest[2],
                    "date_of_birth": guest[3].isoformat(),  # Convert date to ISO format for JSON serialization
                    "bio": guest[4]
                    # Add more guest-related fields as per your requirements
                })
            return jsonify({"message": "Guest not found"}), 404

        elif request.method == 'PUT':
            data = request.json
            name = data.get('name')
            gender = data.get('gender')
            date_of_birth = data.get('date_of_birth')
            bio = data.get('bio')
            # Update more guest-related fields as per your requirements

            cur = mysql.connection.cursor()
            cur.execute("UPDATE Guest SET name=%s, gender=%s, date_of_birth=%s, bio=%s WHERE id=%s",
                        (name, gender, date_of_birth, bio, guest_id))
            mysql.connection.commit()
            cur.close()

            return jsonify({"message": "Guest updated successfully"}), 200

        elif request.method == 'DELETE':
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM Guest WHERE id = %s", (guest_id,))
            mysql.connection.commit()
            cur.close()

            return jsonify({"message": "Guest deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv('PORT'))
