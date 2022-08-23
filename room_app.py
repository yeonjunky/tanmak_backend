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
    emit('message', {'message': 'successfully connected!'})
    emit('connected')


@socketio.on('disconnect')
def disconnect():
    global meatballWorker, player_exist, rooms_dict

    id = request.sid

    for r in rooms(id):
        leave_room(r)
        if r != id:
            del rooms_dict[r][id]

    print('disconnected user: ' + id)

    emit('leaveUser', id, broadcast=True)

    if not players:
        player_exist = False
        meatballWorker.stop()


@socketio.on('createRoom')
def create_room():
    global meatballWorker, player_exist, rooms_dict

    id = request.sid
    room = id + "'s room"
    initial_time = time.time()
    color = '#' + str(hex(random.randint(0, 16777215)))[2:]
    user = Player(id, color, INITIAL_POSITION_RATIO, INITIAL_POSITION_RATIO, room)

    send({'message': id + ' has entered the room.'}, to=room, broadcast=True)

    join_room(room)
    rooms_dict[room] = {id: user}

    emit('initInfo', user.toJson())
    emit('userJoin', user.toJson(), include_self=False, to=room, broadcast=True)

    if not player_exist or not meatballWorker:
        player_exist = True

        meatballWorker = MeatballWorker(socketio, initial_time)
        socketio.start_background_task(meatballWorker.work)

    if not meatballWorker.is_stopped():
        meatballWorker.restart(initial_time)


@socketio.on('join')
def participate_room(data):
    global meatballWorker, player_exist, rooms_dict

    id = request.sid
    room = data['room']
    color = '#' + str(hex(random.randint(0, 16777215)))[2:]
    user = Player(id, color, INITIAL_POSITION_RATIO, INITIAL_POSITION_RATIO, room)

    join_room(room)
    send({'message': id + ' has entered the room.'}, to=room, broadcast=True)
    print(rooms_dict)
    for p in rooms_dict[room]:
        if rooms_dict[room][p].is_alive:
            emit('userJoin', rooms_dict[room][p].toJson())

    rooms_dict[room][id] = user

    emit('initInfo', user.toJson())
    emit('userJoin', user.toJson(), include_self=False, to=room, broadcast=True)

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
def send_user_info(data):
    global rooms_dict

    id = data['id']
    room = data['room']
    player = rooms_dict[room][id]

    player.setPosRatio(data['xRatio'], data['yRatio'])

    emit('update', player.toJson(), broadcast=True, include_self=False)


@socketio.on('dead')
def player_dead(data):
    global meatballWorker, rooms_dict

    id = data['id']
    room = data['room']

    rooms_dict[room][id].is_alive = False

    emit('dead', id, broadcast=True, include_self=False)

    for p in rooms_dict[room]:
        if rooms_dict[room][p].is_alive:
            return 

    meatballWorker.stop()

@app.route('/rooms', methods=['GET', 'POST'])
def all_rooms():
    global rooms_dict

    if not rooms_dict:
        response = {'rooms': None}
    else:
        response = {'rooms': list(rooms_dict)}

    return response


print("server is running on http://localhost:8080")
socketio.run(app, port=8080, host='0.0.0.0')
