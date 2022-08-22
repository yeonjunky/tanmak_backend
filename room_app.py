from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room, send, rooms

import random
import time

from player import Player
from MeatballWorker import MeatballWorker
from constants import INITIAL_POSITION_RATIO


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')
players = {}
rooms_dict = {}
initial_time = 0
player_exist = False
meatballWorker = None
ball_speed = 0
room_name = "asdf"

@socketio.on('connect')
def connect():
    print(socketio.server.manager.rooms['/'].keys())
    emit('connected', {'rooms': str(rooms_dict)})


@socketio.on('disconnect')
def disconnect():
    global meatballWorker, player_exist

    id = request.sid
    room = rooms(id)[1]
    del rooms_dict[room][id]

    print(rooms(id))
    for r in rooms(id):
        leave_room(r)
    print("disconnected user: " + id)

    emit('leaveUser', id, broadcast=True)

    if not players:
        player_exist = False
        meatballWorker.stop()

@socketio.on('join')
def joinRoom():
    global meatballWorker, player_exist

    id = request.sid
    room = id + "'s room"
    initial_time = time.time()
    color = '#' + str(hex(random.randint(0, 16777215)))[2:]
    user = Player(id, color, INITIAL_POSITION_RATIO, INITIAL_POSITION_RATIO)

    join_room(room)
    send({'message': id + ' has entered the room.'}, to=room, broadcast=True)

    if not room in rooms_dict:
        rooms_dict[room] = {}

    for p in rooms_dict[room]:
        if rooms_dict[p].is_alive:
            emit('userJoin', rooms_dict[p].toJson())

    rooms_dict[room][id] = user

    emit('initInfo', user.toJson())
    emit('userJoin', user.toJson(), include_self=False, to=room_name, broadcast=True)

    if not player_exist or not meatballWorker:
        player_exist = True

        meatballWorker = MeatballWorker(socketio, initial_time)
        socketio.start_background_task(meatballWorker.work)

    if not meatballWorker.is_stopped():
        meatballWorker.restart(initial_time)


@socketio.on('leave')
def leave():
    """
    leave room when received leave event
    """

    # if rooms_dict[room]
    pass


@socketio.on('sendUserInfo')
def sendUserInfo(data):
    id = data['id']

    player = rooms_dict[rooms(id)[1]][id]

    player.setPosRatio(data['xRatio'], data['yRatio'])

    emit('update', player.toJson(), broadcast=True, include_self=False)


@socketio.on('dead')
def player_dead(id):
    global meatballWorker

    room = rooms(id)[1]
    rooms_dict[room][id].is_alive = False

    emit('dead', id, broadcast=True, include_self=False)

    for p in rooms_dict[room]:
        if rooms_dict[room][p].is_alive:
            return 

    meatballWorker.stop()

@app.route('/rooms', methods=['GET', 'POST'])
def all_rooms():
    if not rooms_dict:
        response = {'rooms': None}
    else:
        response = {'rooms': list(rooms_dict)}

    return response


print("server is running on http://localhost:8080")
socketio.run(app, port=8080, host='0.0.0.0')
