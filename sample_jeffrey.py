from flask import Flask, request
from json import dumps

app = Flask(__name__)

@app.route('/echo/post', methods = ['POST'])
def echo_post():
    echo_input = request.form.get('echo')
    return dumps({'echo': echo_input})

@app.route('/echo/get', methods = ['GET'])
def echo_get():
    echo_input = requets.args.get('echo')
    return dumps({'echo': echo_input})

@app.route('/auth/register', methods = ['POST'])
def auth_register():
    

if __name__ == '__main__':
    app.run()