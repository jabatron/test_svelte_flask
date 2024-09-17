from flask import Flask, jsonify, request, send_from_directory, session, make_response
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta, timezone
import secrets

app = Flask(__name__, static_folder='../f/dist', static_url_path='')
CORS(app, supports_credentials=True)  # Permitir solicitudes de front-end desde un origen diferente (en desarrollo)
SECRET_KEY = secrets.token_hex(16)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SECRET_KEY'] = SECRET_KEY

@app.after_request
def set_secure_cookie(response):
    session.permanent = True
    response.set_cookie('session', secure=True, httponly=True, samesite='Lax')
    return response

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# Ruta de login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if email == "user@example.com" and password == "zaqxswedc":
        token = jwt.encode({
            'user_id': email,
            'exp': datetime.now(tz=timezone.utc) + timedelta(minutes=15)
        }, SECRET_KEY, algorithm='HS256')
        resp = make_response(jsonify({'message': 'Login successful'}))
        resp.set_cookie('token', token, secure=False)
        #resp.set_cookie('token', token, httponly=True, secure=True, samesite='Lax', path='/')
        print (resp.headers)
        return resp
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# Ruta protegida
@app.route('/protected', methods=['POST'])
def protected():
    token = request.cookies.get('token') 
    print('Cookies', request.cookies)
    print('El token es', token)
    if token:
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return jsonify({"message": f"Welcome, {decoded['user_id']}!"}), 200
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401
    else:
        return jsonify({"message": "Token is missing"}), 403

if __name__ == '__main__':
    app.run(debug=True)
