export class Player {
    constructor(id, color, isMy = false, document) {
        this.id = id;
        this.name = "hello";
        this.color = color;
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

    init(xRatio, yRatio) {
        const speedConstant = 3 / 800;
        const radiusConstant = 10 / (800 * 800);
        this.playerXSpeed = this.stageWidth * speedConstant;
        this.playerYSpeed = this.stageHeight * speedConstant;
        this.radius = this.stageWidth * this.stageHeight * radiusConstant;
        this.setX(xRatio);
        this.setY(yRatio);
    }

    resize(stageWidth, stageHeight) {
        const previousXRatio = this.getXRatio();
        const previousYRatio = this.getYRatio();

        this.stageWidth = stageWidth;
        this.stageHeight = stageHeight;

        this.init(previousXRatio, previousYRatio);
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
        if (this.x === undefined) return 0.5;
        return this.x / this.stageWidth;
    }

    setX(xRatio) {
        this.x = this.stageWidth * xRatio;
    }

    getYRatio() {
        if (this.y === undefined) return 0.5;
        return this.y / this.stageHeight;
    }

    setY(yRatio) {
        this.y = this.stageHeight * yRatio;
    }

    update() {
        if (this.isMy) {
            if (this.rightPressed && this.x < this.stageWidth - this.radius) this.x += this.playerXSpeed;
            if (this.leftPressed && this.x > this.radius) this.x -= this.playerXSpeed;
            if (this.upPressed && this.y > this.radius) this.y -= this.playerYSpeed;
            if (this.downPressed && this.y < this.stageHeight - this.radius) this.y += this.playerYSpeed;
        }
    }

}