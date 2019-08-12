from flask import render_template, redirect
from app import app
# from app.search import Name


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/face')
def face():
    dataFace = {
        'link': 'https://i.ytimg.com/vi/GAnQGc-Ce_o/hqdefault.jpg',
        'name': 'Faza Ghassani'
    }

    return render_template('face.html', face=dataFace)


@app.route('/fingerprint')
def fingerprint():
    # if Name:
    #     dataFinger = {
    #         'link': 'https://i.ytimg.com/vi/GAnQGc-Ce_o/hqdefault.jpg',
    #         'name': Name
    #     }
    # else:
    #     return redirect('access_denied.html', change=False)
    dataFinger = {}
    return render_template('fingerprint.html', fingerprint=dataFinger)


@app.route('/access_denied')
def access_denied():
    return render_template('access_denied.html')