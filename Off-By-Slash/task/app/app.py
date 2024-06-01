from flask import Flask, request, render_template

app = Flask(__name__, template_folder='templates')

real_flag = ''

with open('./flag.txt') as flag_file:
    real_flag = flag_file.read().strip()

@app.route('/')
def index():
    return render_template('index.html')    


@app.route('/submit_flag/<flag>', methods=['GET'])
@app.route('/submit_flag', defaults={'flag': None}, methods=['POST'])
def flag(flag):
    if request.method == 'POST':
        flag = request.form['flag']
    return render_template('right.html', flag=flag) if flag == real_flag else render_template('wrong.html') 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
