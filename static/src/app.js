import { Player } from "./player.js";
import { PlayerGroup } from "./playerGroup.js";

class App {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
        document.body.appendChild(this.canvas);

        this.socket = io("http://localhost:8000");
        this.playerGroup = new PlayerGroup(this.socket);
        this.socket.on('initInfo', function (data) {
            console.log("adsf")
            data = JSON.parse(data)
            this.myPlayer = new Player(data.id, data.color, true, document);
            this.playerGroup.addPlayer(this.myPlayer);
            window.addEventListener('resize', this.resize.bind(this), false);
            this.resize('resize');
        }.bind(this));

        requestAnimationFrame(this.update.bind(this));
    }

    resize() {
        this.stageWidth = this.canvas.clientWidth;
        this.stageHeight = this.canvas.clientHeight;

        const dpr = window.devicePixelRatio;

        this.playerGroup.resize(this.stageWidth, this.stageHeight);
        
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
