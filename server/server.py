import threading

from flask import Flask, jsonify

import config.config as CONFIG
from sec_levels.DefconHandler import DefconHandler

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello, World!"


@app.route('/increase_security_level')
def increase_security_level():
    defcon_handler = DefconHandler()
    defcon_handler.increase()
    return "Success"


@app.route('/decrease_security_level')
def decrease_security_level():
    defcon_handler = DefconHandler()
    defcon_handler.decrease()
    return "Success"


@app.route('/get_security_level', methods=['GET'])
def get_security_level():
    defcon_handler = DefconHandler()
    criticality = defcon_handler.getSecurityLevel().value
    if criticality and criticality >= 0:
        return jsonify(criticality=criticality)
    else:
        return jsonify(error="Could not get criticality"), 404


@app.route('/get_parent_ip', methods=['GET'])
def get_parent_ip():
    parent_ip = CONFIG.parent_ip
    if parent_ip and parent_ip != '':
        return jsonify(parent_ip=parent_ip)
    else:
        return jsonify(error="Parent not found"), 404


@app.route('/get_child_ips', methods=['GET'])
def get_child_ips():
    child_ips = CONFIG.child_ips
    if child_ips and len(child_ips) > 0:
        return jsonify(child_ips=child_ips)
    else:
        return jsonify(error="Parent not found"), 404


def run_server_process():
    app.run(host='0.0.0.0', port=5000)


def start_flask_server():
    threading.Thread(target=run_server_process).start()
