from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')
real_flag = ''


with open('./flag.txt') as flag_file:
    real_flag = flag_file.read().strip()


@app.route('/')
def index():
    return render_template('index.html', flag=real_flag)


@app.route('/submit_flag/<flag>', methods=['GET'])
def flag(flag):
    return real_flag if flag == real_flag else 'Not correct!'


if __name__ == '__main__':
    app.run()
