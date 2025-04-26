from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from utils import generate_token, verify_token
from auth import check_login

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    print("================================")
    print(email)
    if check_login(email, password):
        token = generate_token(email)
        response = make_response(jsonify({'success': True}))
        response.set_cookie('token', token, httponly=True, secure=False, samesite='Lax')  # set secure=True untuk production
        return response
    return jsonify({'success': False, 'message': 'Email atau password salah'}), 401

@app.route('/api/protected', methods=['GET'])
def protected():
    token = request.cookies.get('token')
    user = verify_token(token)
    if user:
        print("USERRRR:",user)
        return jsonify({'success': True, 'email': user['email']})
        
    return jsonify({'success': False, 'message': 'Tidak ada akses'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({'success': True}))
    response.set_cookie('token', '', expires=0)
    return response

if __name__ == '__main__':
    app.run(debug=True)
