from flask import Flask, request, render_template, render_template_string

app = Flask(__name__, template_folder='templates')
real_flag = 'awda'


with open('./flag.txt') as flag_file:
    real_flag = flag_file.read().strip()


@app.route('/submit_flag/<flag>', methods=['GET'])
def flag(flag):
    return real_flag if flag == real_flag else 'Not correct!'

@app.route('/')
def home():
    return '''
        <h1>Welcome to the Vulnerable Flask App!</h1>
        <form method="post" action="/greet">
            <label for="name">Enter your name:</label>
            <input type="text" id="name" name="name">
            <input type="submit" value="Submit">
        </form>
    '''

@app.route('/greet', methods=['POST'])
def greet():
    name = request.form['name']
    template = f'''
        <h1>Hello, {name}!</h1>
        <p>Thank you for visiting our site.</p>
    '''
    return render_template_string(template)


if __name__ == '__main__':
    app.run(debug=True)
