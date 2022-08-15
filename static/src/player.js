export class Player {
    constructor(stageWidth, stageHeight, xRatio, yRatio, id, color, isMy = false, document) {
        this.stageWidth = stageWidth;
        this.stageHeight = stageHeight;

        this.id = id;
        this.name = "hello";
        this.x = this.stageWidth * xRatio;
        this.y = this.stageHeight * yRatio;
        this.radius = 10;
        this.color = color;
        this.playerSpeed = 3;
        this.dead = false;
        this.isMy = isMy;

        if (isMy) {
            this.rightPressed = false;
            this.leftPressed = false;
            this.upPressed = false;
            this.downPressed = false;
            document.addEventListener('keydown', this.keyDownHandler.bind(this), false);
            document.addEventListener('keyup', this.keyUpHandler.bind(this), false);
        }
    }

    keyDownHandler(event) {
        if (event.code == 'ArrowRight') this.rightPressed = true;
        if (event.code == 'ArrowLeft') this.leftPressed = true;
        if(event.code == "ArrowDown") this.downPressed = true;
        if(event.code == "ArrowUp") this.upPressed = true;
    }
    
    keyUpHandler(event) {
        if (event.code == 'ArrowRight') this.rightPressed = false;
        if (event.code == 'ArrowLeft') this.leftPressed = false;
        if(event.code == "ArrowDown") this.downPressed = false;
        if(event.code == "ArrowUp") this.upPressed = false;
    }

    getX() {
        return this.x;
    }

    getY() {
        return this.y;
    }

    getXRatio() {
        return this.x / this.stageWidth;
    }

    setX(xRatio) {
        this.x = this.stageWidth * xRatio;
    }

    getYRatio() {
        return this.y / this.stageHeight;
    }

    setY(yRatio) {
        this.x = this.stageHeight * yRatio;
    }

    update() {
        if (this.isMy) {
            if (this.rightPressed && this.x < this.stageWidth - this.radius) this.x += this.playerSpeed;
            if (this.leftPressed && this.x > this.radius) this.x -= this.playerSpeed;
            if (this.upPressed && this.y > this.radius) this.y -= this.playerSpeed;
            if (this.downPressed && this.y < this.stageHeight - this.radius) this.y += this.playerSpeed;
        }
    }

}
