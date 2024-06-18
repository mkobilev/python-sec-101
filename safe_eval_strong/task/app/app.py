from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__, template_folder='templates')
real_flag = ''

with open('./flag.txt') as flag_file:
    real_flag = flag_file.read().strip()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_flag/<flag>', methods=['GET'])
def flag(flag):
    return real_flag if flag == real_flag else 'Not correct!'


ALLOWED_NAMES = {
    'abs': abs,
    'round': round,
    'sum': sum,
    'math': math,
}

def is_allowed_expr(expr):
    for char in expr:
        print(char)
        if not (char.isdigit() or char in ' +-*/().'):
            return False
    return True


def safe_eval(expr):
    print(dir(round))
    try:
        code = compile(expr, "<string>", "eval")
        
        print('code', code)
        print('code.co_names', code.co_names)

        if len(code.co_names) > 0:
            cmd = code.co_names[0]
            if cmd not in ALLOWED_NAMES:
                raise ValueError(f"Use of '{cmd}' is not allowed")

        result = eval(code)
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
    app.run(debug=True, port=8888)
