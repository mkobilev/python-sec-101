from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'flag': "PODLODKA{'NOT_TRUST_PR0XY'}"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=80)
