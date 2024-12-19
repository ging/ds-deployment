from flask import Flask, request, jsonify
import json
import time

app = Flask(__name__)

@app.route('/transfers/<id>/start', methods=['POST', 'GET'])
def receive_data(id):
    print(id)
    return "ok"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)