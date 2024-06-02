from flask import Flask, request, render_template, redirect, make_response, jsonify
import jwt
import time
import secrets
import string


app = Flask(__name__, template_folder='templates')

real_flag = ''


with open('./flag.txt') as flag_file:
    real_flag = flag_file.read().strip()


def generate_super_random_string(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(secrets.choice(characters) for i in range(length))
    return random_string


super_random_string = generate_super_random_string(32)

print(generate_super_random_string(32))
print(generate_super_random_string(32))
print(generate_super_random_string(32))
print(generate_super_random_string(32))

def generate_jwt_token(user_name: str):
    payload = {
        "user_name": user_name,
        "exp": int(time.time()) + 3600
    }
    # token = jwt.encode(payload, super_random_string, algorithm='HS256')
    token = jwt.encode(payload, None, algorithm=None)
    return token


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'password':
            token = generate_jwt_token(username)
            resp = make_response(redirect('/profile'))
            resp.set_cookie('Authorization', token)
            return resp
        else:
            return "Invalid credentials", 401
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin':
            return "Access denied!", 403
    
        token = generate_jwt_token(username)
        
        resp = make_response(redirect('/profile'))
        resp.set_cookie('Authorization', token)
        return resp
    return render_template('register.html')


@app.route('/profile')
def profile():
    options = {
        "verify_signature": '',
        "algorithms": ['HS256'],
        "keys": [
            'yZsSfyHRiVvZW#yjJgjSsq^&amp;cl$vU8e#', 
            'EbCw0XQ1U^aKLX5BLZ#hQ1w5v5W^mPqL',
            '#rPloFjP8^zFOW8@qsxYbcoMcA8qfZ@j',
            'mzkcCzhvD3fM^YJVtGhTMt#YPREdMY$E',
        ]
    }
    token = request.cookies.get('Authorization')

    if not token:
        return jsonify({'message': 'Token is missing'}), 401
    try:
        decoded = jwt.decode(token, options=options)
        user_name = decoded['user_name']
        print('decoded', decoded)
        if user_name == 'admin':
            return render_template('profile.html', flag=real_flag)
        else:
            return f"Welcome, User {user_name}!", 200
    except jwt.InvalidTokenError:
        return "Invalid token", 403


@app.route('/submit_flag/<flag>', methods=['GET'])
def flag(flag):
    return real_flag if flag == real_flag else 'Not correct!'


if __name__ == '__main__':
    app.run(debug=True, port=8888)