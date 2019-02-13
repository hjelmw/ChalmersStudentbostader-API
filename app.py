from flask import Flask, jsonify, request
from aptus import unlockdoor

app = Flask(__name__)

@app.route('/opendoor', methods=['POST'])
def opendoor():
    if (request.method != 'POST'):
        return jsonify(response = 'Not allowed. please use POST', status = 405)

    usr = request.form['usr']
    pwd = request.form['pwd']
    door_id = request.form['door_id']
    res = unlockdoor(usr, pwd, door_id)

    return jsonify(
        response = res,
        status = 200,
        mimetype = 'application/json'
    )
