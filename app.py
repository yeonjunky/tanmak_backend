from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from engineio.payload import Payload

import random

from player import Player


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
Payload.max_decode_packets = 100
socketio = SocketIO(app, cors_allowed_origins='*')

INITIAL_POSITION_RATIO = 0.5

players = {}

@socketio.event
def connect():
    id = request.sid
    color = '#' + str(hex(random.randint(0, 16777215)))[2:]

    user = Player(id, color, INITIAL_POSITION_RATIO, INITIAL_POSITION_RATIO)

    for p in players:
        emit('userJoin', players[p].toJson())

    emit('initInfo', user.toJson())
    players[id] = user
    print(players, 'sadf')

    emit('userJoin', user.toJson(), broadcast=True, include_self=False)


@socketio.on('disconnect')
def disconnect():
    id = request.sid
    del players[id]
    print("disconnected user: " + id)
    emit('leaveUser', id, broadcast=True)


@socketio.on('sendUserInfo')
def sendUserInfo(data):
    player = players[data['id']]

    player.xRatio = data['xRatio']
    player.yRatio = data['yRatio']

    emit('update', player.toJson(), broadcast=True, include_self=False)


@app.route('/')
def index():
    return render_template('index.html')


print("server is running on http://localhost:8000")
socketio.run(app, port=8000)
