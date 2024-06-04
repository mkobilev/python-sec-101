from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    send_file,
    abort,
    session,
)
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__, template_folder='templates')
app.secret_key = 'sdfsdfsdfsdf'
real_flag = ''


app.config['UPLOAD_FOLDER'] = './uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

with open('./flag.txt') as flag_file:
    real_flag = flag_file.read().strip()


@app.route('/submit_flag/<flag>', methods=['GET'])
def flag(flag):
    return real_flag if flag == real_flag else 'Not correct!'


users = {'admin': generate_password_hash('password')}

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user_dir = app.config['UPLOAD_FOLDER'] + '/' + session['username']
    os.makedirs(user_dir, exist_ok=True)
    files = os.listdir(user_dir)

    return render_template('home.html', files=files)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return 'User already exists!'
        users[username] = generate_password_hash(password)
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users or not check_password_hash(users[username], password):
            return 'Invalid credentials!'
        session['username'] = username
        return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    # Удаление данных пользователя из сессии
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            a = session.get('tmp')
            print('a', a)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/' + session['username'], filename))
            flash(f"File '{filename}' uploaded successfully.")
            return redirect(url_for('home'))


@app.route('/view', methods=['GET'])
def view_image():
    if 'username' not in session:
        return redirect(url_for('login'))

    filename = request.args.get('filename')
    if not filename:
        abort(400)

    file_path = os.path.join(app.config['UPLOAD_FOLDER'] + '/' + session['username'], filename)
    print("", file_path)
    try:
        return send_file(file_path, mimetype='image/jpeg')
    except FileNotFoundError:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)
