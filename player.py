class Player:
    def __init__(self, id, color, xRatio, yRatio) -> None:
        self.id = id
        self.color = color
        self.xRatio = xRatio
        self.yRatio = yRatio
        self.is_alive = True

    def setPosRatio(self, xRatio, yRatio):
        self.xRatio = xRatio
        self.yRatio = yRatio

    def toJson(self):
        return {
            'id': self.id, 
            'color': self.color, 
            'xRatio': self.xRatio, 
            'yRatio': self.yRatio
        }