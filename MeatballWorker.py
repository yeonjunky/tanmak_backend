import time
import random

from tanmak import MeatBall
from constants import NEXT_BALL_DELAY

class MeatballWorker:
    next_ball_delay = NEXT_BALL_DELAY

    def __init__(self, socketio, initial_time) -> None:
        self.socketio = socketio
        self.flag = False
        self.initial_time = initial_time

    def work(self):
        self.flag = True

        while self.flag:
            curr_time = time.time()

            if random.randint(0, 1): # 0 -> xRatio = 0, 1 -> yRatio = 0
                xRatio = 0
                yRatio = random.random()

            else:
                xRatio = random.random()
                yRatio = 0

            speed = MeatBall.get_speed(self.initial_time, curr_time)

            self.socketio.emit('meatBall', MeatBall(xRatio, yRatio, speed).toJson(), broadcast=True)

            delay_idx = int((curr_time - self.initial_time) // 10)

            if delay_idx >= len(self.next_ball_delay):
                delay_idx = len(self.next_ball_delay) - 1

            self.socketio.sleep(self.next_ball_delay[delay_idx])

    def stop(self):
        self.flag = False

    def restart(self, initial_time):
        self.flag = True
        self.set_initial_time(initial_time)

    def set_initial_time(self, initial_time):
        self.initial_time = initial_time

    def is_stopped(self):
        return not self.flag

    # def 