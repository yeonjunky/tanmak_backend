import json

class Player:
    def __init__(self, id, color, xRatio, yRatio) -> None:
        self.id = id
        self.color = color
        self.xRatio = xRatio
        self.yRatio = yRatio

    def setPosRatio(self, xRatio, yRatio):
        self.xRatio = xRatio
        self.yRatio = yRatio

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)