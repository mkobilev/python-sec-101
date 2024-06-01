from flask import Flask, request, jsonify
from itertools import chain
from urllib.parse import unquote
from ast import literal_eval
import pyjsparser.parser
import js2py
import traceback
import requests

class Api:
    def hello(self, name):
       return f"Hello {name}"
    
    def eval_js(self, script, es6):
        js = requests.get(script).text
        return (js2py.eval_js6 if es6 else js2py.eval_js)(js)

app = Flask(__name__)
api = Api()
real_flag = ''
with open('/flag.txt') as flag_file:
    real_flag = flag_file.read().strip()

@app.route('/api/<func>', methods=['GET', 'POST'])
@app.route('/api/<func>/<args>', methods=['GET', 'POST'])
def rpc(func, args=""):
    try: # Setup and logging for security
        pyjsparser.parser.ENABLE_PYIMPORT = True
        ip = request.remote_addr
        client = ip if ip != '127.0.0.1' else ip.local
        app.logger.debug(f"Request coming from {client}")
        pyjsparser.parser.ENABLE_PYIMPORT = False
    except Exception as exc:
        jsonify(error=str(exc), traceback=traceback.format_exc()), 500

    args = unquote(args).split(",")
    print(args)
    if len(args) == 1 and not args[0]:
        args = []

    kwargs = {}
    for x, y in chain(request.args.items(), request.form.items()):
        kwargs[x] = unquote(y)

    try:
        response = jsonify(getattr(api, func)(
            *[literal_eval(x) for x in args],
            **{x: literal_eval(y) for x, y in kwargs.items()},
        ))
    except Exception as exc:
        response = jsonify(error=str(exc), traceback=traceback.format_exc()), 500
    return response

@app.route('/submit_flag/<flag>', methods=['GET'])
def flag(flag):
    return real_flag if flag == real_flag else 'Not correct!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
