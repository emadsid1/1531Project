from flask import Flask, request
from json import dumps

app = Flask(__name__)

# global varaiables
messages = {
    'channal_1' = [],
}
# end of global variable

@app.route('/echo/post', methods = ['POST'])
def echo_post():
    echo_input = request.form.get('echo')
    return dumps({'echo': echo_input})

@app.route('/echo/get', methods = ['GET'])
def echo_get():
    echo_input = requets.args.get('echo')
    return dumps({'echo': echo_input})

@app.route('/message/sendlater', methods=['POST'])


@app.route('/message/send', methods=['POST'])


@app.route('/message/remove', methods=['DELET'])


@app.route('/message/edit', methods=['PUT'])


@app.route('/message/react', methods=['POST'])


@app.route('/message/unreact', methods=['POST'])


@app.route('/message/pin', methods=['POST'])


@app.route('/message/unpin', methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)
