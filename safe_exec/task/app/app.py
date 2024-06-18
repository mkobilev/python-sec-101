from flask import Flask, render_template, request, jsonify

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

BLACK_LIST = ['eval', 'exec', 'import', 'open', 'os', 'read', 'system', 'write']

@app.route('/calc', methods=['POST'])
def calc():
    command = request.form.get('command')

    if not command:
        return jsonify({'error': 'No command provided'}), 400    
    
    for cmd in BLACK_LIST:
        if cmd in command:
            return "Access denied!", 403
    try:
        result = exec(command)
    except Exception as ex:
        result = str(ex)
    
    return render_template("result.html", result=result)


if __name__ == '__main__':
    app.run(debug=False)
