from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/proxy', methods=['GET'])
def proxy():
    url = request.args.get('url')
    if not url:
        return "Missing 'url' parameter.", 400

    try:
        response = requests.get(url)
        return render_template('proxy.html', content=response.content.decode('utf-8'))
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
