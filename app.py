from flask import Flask, request
from flask_socketio import SocketIO, emit

import random
import time

from player import Player
from MeatballWorker import MeatballWorker

INITIAL_POSITION_RATIO = 0.5


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')
players = {}
initial_time = 0
player_exist = False
meatballWorker = None


@socketio.on('connect')
def connect():
    global player_exist, meatballWorker

    initial_time = time.time()
    id = request.sid
    color = '#' + str(hex(random.randint(0, 16777215)))[2:]
    user = Player(id, color, INITIAL_POSITION_RATIO, INITIAL_POSITION_RATIO)

    print("sdaf", id)
    for p in players:
        emit('userJoin', players[p].toJson())

    players[id] = user

    emit('initInfo', user.toJson())
    emit('userJoin', user.toJson(), broadcast=True, include_self=False)

    if not player_exist:
        player_exist = True
        meatballWorker = MeatballWorker(socketio, initial_time)
        socketio.start_background_task(meatballWorker.work)


@socketio.on('disconnect')
def disconnect():
    global player_exist, meatballWorker

    id = request.sid
    del players[id]
    print("disconnected user: " + id)
    emit('leaveUser', id, broadcast=True)

    if not players:
        player_exist = False
        meatballWorker.stop()


@socketio.on('sendUserInfo')
def sendUserInfo(data):
    player = players[data['id']]

    player.setPosRatio(data['xRatio'], data['yRatio'])

    emit('update', player.toJson(), broadcast=True, include_self=False)


@socketio.on('dead')
def player_dead(id):
    emit('dead', id, broadcast=True)


print("server is running on http://localhost:8080")
socketio.run(app, port=8080, host='0.0.0.0')
