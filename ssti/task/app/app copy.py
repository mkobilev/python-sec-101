from flask import Flask, request, render_template, redirect, url_for, session, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
from collections import defaultdict

app = Flask(__name__)
app.secret_key = (
    'supersecretkey'  # Используйте более сложный ключ в реальном приложении
)

# Простая база данных пользователей и отзывов
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
        user_reviews[username] = []  # Создаем запись для отзывов нового пользователя
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
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/reviews', methods=['GET'])
def reviews_page():
    if 'username' not in session:
        return redirect(url_for('login'))

    user_reviews_list = user_reviews[session['username']]
    
    # Демонстрация SSTI уязвимости
    reviews_html = '<br>'.join(user_reviews_list)
    
    # print(f'{reviews_html}')
    # a = f'''{reviews_html}'''
    # return render_template('reviews.html', reviews_html=a)
    
    reviews_html = ''.join([f"<p>{review}</p>" for review in user_reviews_list])
    print(reviews_html)
    return render_template_string(
        f'''
    {{% extends "base.html" %}}
    {{% block title %}}Reviews{{% endblock %}}
    {{% block content %}}
    <h1>Reviews</h1>
    {reviews_html}
    <h2>Leave a Review</h2>
    <form method="post" action="{{{{ url_for('add_review') }}}}">
        <label for="review">Review:</label>
        <textarea id="review" name="review"></textarea>
        <input type="submit" value="Submit">
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
