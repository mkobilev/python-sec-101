import secrets
import string
import time

import jwt
from flask import Flask, make_response, redirect, render_template, request, url_for

app = Flask(__name__, template_folder='templates')
app.secret_key = 'super secret key'

real_flag = ''


with open('./flag.txt') as flag_file:
    real_flag = flag_file.read().strip()


def generate_super_random_string(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(secrets.choice(characters) for i in range(length))
    return random_string


super_random_string = generate_super_random_string(32)

def generate_jwt_token(user_name: str):
    payload = {
        "user_name": user_name,
        "exp": int(time.time()) + 3600
    }
    token = jwt.encode(payload, super_random_string, algorithm='HS256')
    # token = jwt.encode(payload, None, algorithm=None)
    return token


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin':
            return "Only for Admin!", 403

        token = generate_jwt_token(username)

        response = make_response(redirect(url_for('profile')))
        response.set_cookie('token', token)
        return response

    return render_template('register.html')


@app.route('/profile')
def profile():
    token = request.cookies.get('token')
    if not token:
        return "Access denied", 402

    try:
        header = jwt.get_unverified_header(token)
        decoded = jwt.decode(token, super_random_string, algorithms='HS256', options={'verify_signature': header['alg'] != 'none'})
    except jwt.InvalidTokenError:
        return "Invalid token", 403

    user_name = decoded['user_name']
    if user_name == 'admin':
        return render_template('admin.html', {'flag': real_flag})

    return f"Welcome, User {user_name}!", 200


@app.route('/submit_flag/<flag>', methods=['GET'])
def flag(flag):
    return real_flag if flag == real_flag else 'Not correct!'


if __name__ == '__main__':
    app.run(debug=True, port=8888)
