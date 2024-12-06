from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello, World!"


@app.route('/json', methods=['GET'])
def json_response():
    return jsonify(message="This is a JSON response!")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
