from flask import Flask, request
from flask_socketio import SocketIO, emit

import random

from player import Player

INITIAL_POSITION_RATIO = 0.5


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')
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

    player.setPosRatio(data['xRatio'], data['yRatio'])

    emit('update', player.toJson(), broadcast=True, include_self=False)


print("server is running on http://localhost:8080")
socketio.run(app, port=8080)
