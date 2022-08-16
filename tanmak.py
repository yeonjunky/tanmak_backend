import math
import random

class MeatBall:
    def __init__(self, xRatio, yRatio, speed) -> None:
        self.xRatio = xRatio
        self.yRatio = yRatio
        self.angle = random.randint(0, 360)
        self.xDriection = math.sin(self.angle)
        self.yDriection = math.cos(self.angle)
        self.speed = speed

    @staticmethod
    def get_speed(initial_time, curr_time):
        return (3 + 0.5 * ((curr_time - initial_time) // 20)) / 800

    def toJson(self):
        return {
            'xRatio': self.xRatio,
            'yRatio': self.yRatio,
            'xDirection': self.xDriection,
            'yDirection': self.yDriection,
            'speed': self.speed
        }