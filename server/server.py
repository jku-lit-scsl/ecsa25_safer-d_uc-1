from flask import Flask, jsonify

import config.config as CONFIG

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello, World!"


@app.route('/get_parent_ip', methods=['GET'])
def get_parent_ip():
    parent_ip = CONFIG.parent_ip
    if parent_ip and parent_ip != '':
        return jsonify(server=parent_ip)
    else:
        return jsonify(error="Parent not found"), 404


@app.route('/get_child_ips', methods=['GET'])
def get_child_ips():
    child_ips = CONFIG.child_ips
    if child_ips and len(child_ips) > 0:
        return jsonify(server=child_ips)
    else:
        return jsonify(error="Parent not found"), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
