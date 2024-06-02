from flask import Flask, request, render_template, redirect, url_for, session, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
from collections import defaultdict

app = Flask(__name__)
app.secret_key = (
    'supersecretkey'
)

users = {'admin': generate_password_hash('password')}
user_reviews = defaultdict(list)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return 'User already exists!'
        users[username] = generate_password_hash(password)
        user_reviews[username] = []
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
        return redirect(url_for('reviews_page'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/reviews', methods=['GET'])
def reviews_page():
    if 'username' not in session:
        return redirect(url_for('login'))

    user_reviews_list = user_reviews[session['username']]
    
    reviews_html = ''.join([f"<p>{review}</p>" for review in user_reviews_list])
    return render_template_string(
        f'''
    {{% extends "base.html" %}}
    {{% block title %}}Reviews{{% endblock %}}
    {{% block content %}}
    <h1>Отзывы:</h1>
    {reviews_html}
    <h2>Оставьте свой отзыв, чтобы мы работали ещё лучше :)</h2>
    <form method="post" action="{{{{ url_for('add_review') }}}}">
        <div class="form-group">
            <label for="review">Отзыв:</label>
            <textarea id="review" name="review" class="form-control" required/></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Сохранить</button>
    </form>
    {{% endblock %}}
    '''
    )


@app.route('/add_review', methods=['POST'])
def add_review():
    if 'username' not in session:
        return redirect(url_for('login'))

    review = request.form['review']
    user_reviews[session['username']].append(review)
    return redirect(url_for('reviews_page'))


if __name__ == '__main__':
    app.run(debug=True)
