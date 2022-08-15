from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from engineio.payload import Payload

import logging
import random

from player import Player


# logging.getLogger('socketio').setLevel(logging.ERROR)
# logging.getLogger('engineio').setLevel(logging.ERROR)
# logging.getLogger('geventwebsocket.handler').setLevel(logging.ERROR)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
Payload.max_decode_packets = 50
socketio = SocketIO(app, cors_allowed_origins='*')

players = {}

@socketio.on('connect')
def connect():
    id = request.sid
    color = []

    for _ in range(3):
        color.append(random.randint(0, 255))

    data = {
        'xRatio': random.random(),
        'yRatio': random.random(),
        'id': id,
        'color': 'rgb(' + str(color)[1:-1] + ')'
    }

    user = Player(**data)

    for p in players:
        emit('userJoin', players[p].toJson())

    players[id] = user
    emit('userJoin', user.toJson(), broadcast=True)

    emit('initInfo', user.toJson())


@socketio.on('disconnect')
def disconnect():
    id = request.sid
    del players[id]
    emit('leaveUser', id, broadcast=True)


@socketio.on('sendUserInfo')
def sendUserInfo(data):
    player = players[data['id']]

    player.xRatio = data['xRatio']
    player.yRatio = data['yRatio']
    emit('update', player.toJson(), broadcast=True)    


@app.route('/')
def index():
    return render_template('index.html')


print("server is running on http://localhost:8000")
socketio.run(app, port=8000)
