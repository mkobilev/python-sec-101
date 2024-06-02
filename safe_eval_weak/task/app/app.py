from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='templates')
real_flag = ''
import ast

with open('./flag.txt') as flag_file:
    real_flag = flag_file.read().strip()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit_flag/<flag>', methods=['GET'])
def flag(flag):
    return real_flag if flag == real_flag else 'Not correct!'


def safe_eval(expr):
    try:
        result = eval(expr)
    except Exception as e:
        result = str(e)
    return result


@app.route('/calc', methods=['POST'])
def calc():
    command = request.form.get('command')
    if not command:
        return jsonify({'error': 'No command provided'}), 400
    
    result = safe_eval(command)
    
    return render_template("result.html", result=result)



if __name__ == '__main__':
    app.run(debug=True)
