from flask import render_template, request, jsonify, session, redirect, url_for
import json
from app import app
# from app.search import Name

data_finger = None
data_face = None
data_access =None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/post/face', methods=['POST'])
def face_post():
    if request.method == 'POST':
        data = request.json
        link = data['link']
        name = data['name']
        response = {'name': name, 'link': link}
        global data_face
        data_face = json.dumps(response)
        return data_face


@app.route('/face')
def face():
    face = json.loads(data_face)
    return render_template('face.html', face=face)


@app.route('/api/post/fingerprint', methods=['POST'])
def fingerprint_post():
    if request.method == 'POST':
        data = request.json
        link = data['link']
        name = data['name']
        response = {'name': name, 'link': link}
        global data_finger
        data_finger = json.dumps(response)
        return data_finger


@app.route('/fingerprint')
def fingerprint():
    fingerprint = json.loads(data_finger)
    return render_template('fingerprint.html', fingerprint=fingerprint)


@app.route('/api/post/access_denied', methods=['POST'])
def access_denied_post():
    data = request.json
    type = data['type']
    error = data['error']
    response = {'type': type, 'error':error}
    global data_access
    data_access = json.dumps(response)
    return data_access

#
@app.route('/access_denied')
def access_denied():
    denied = json.loads(data_access)
    if 'face' in denied:
        change = False
    else:
        change = True
    return render_template('access_denied.html', change=change)