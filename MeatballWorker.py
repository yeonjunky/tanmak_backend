import time
import random

from tanmak import MeatBall

class MeatballWorker:
    next_ball_delay = [0.8, 0.6, 0.4, 0.2, 0.1, 0.05]

    def __init__(self, socketio, initial_time) -> None:
        self.socketio = socketio
        self.flag = True
        self.initial_time = initial_time

    def work(self):
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

    def set_initial_time(self, initial_time):
        self.initial_time = initial_time