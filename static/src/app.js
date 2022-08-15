import { Player } from "./player.js";
import { PlayerGroup } from "./playerGroup.js";

class App {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
        document.body.appendChild(this.canvas);

        window.addEventListener('resize', this.resize.bind(this), false);
        this.resize('resize');

        this.socket = io("http://localhost:8000");
        this.playerGroup = new PlayerGroup(this.stageWidth, this.stageHeight, this.socket);
        this.socket.on('initInfo', function (data) {
            data = JSON.parse(data)
            this.myPlayer = new Player(this.stageWidth, this.stageHeight, 
                                       data.xRatio, data.yRatio, data.id, data.color, 
                                       true, document);
            this.playerGroup.addPlayer(this.myPlayer);
            // console.log(this.playerGroup);
        }.bind(this));

        requestAnimationFrame(this.update.bind(this));
    }

    resize() {
        this.stageWidth = 500;
        this.stageHeight = 500;

        const dpr = window.devicePixelRatio;
        
        this.canvas.width = this.stageWidth * dpr;
        this.canvas.height = this.stageHeight * dpr;
        this.ctx.scale(dpr, dpr);
    }

    update() {
        this.ctx.clearRect(0, 0, this.stageWidth, this.stageHeight);

        this.playerGroup.update(this.ctx);

        requestAnimationFrame(this.update.bind(this));
    }

}

window.onload = () => {
    new App();
};
