import { Player } from "./player.js";

export class PlayerGroup {
    constructor(stageWidth, stageHeight, socket) {
        this.stageWidth = stageWidth;
        this.stageHeight = stageHeight;
        this.players = {};
        this.socket = socket;

        this.socket.on('userJoin', (data) => {
            data = JSON.parse(data)
            const newPlayer = new Player(this.stageWidth, this.stageHeight, 
                                         data.xRatio, data.yRatio, data.id, data.color);
            this.addPlayer(newPlayer);
            // console.log(this.players);
        });

        this.socket.on('update', (data) => {
            data = JSON.parse(data)
            let player = this.players[data.id];
            player.setX(data.xRatio);
            player.setY(data.yRatio);
        });

        this.socket.on('leaveUser', (id) => {
            delete this.players[id];
        });
    }

    addPlayer(player) {
        this.players[player.id] = player;
    }

    update(ctx) {
        for (const player in this.players) {
            const playerObject = this.players[player];
            if (playerObject.isMy) {
                playerObject.update();
                this.socket.emit('sendUserInfo', {
                    id: player,
                    xRatio: playerObject.getXRatio(),
                    yRatio: playerObject.getYRatio(),
                });
            }
            if (playerObject.dead) {
                delete this.players[player];
                continue;
            }
            ctx.beginPath();
            ctx.fillStyle = playerObject.color;
            ctx.arc(playerObject.getX(), 
                    playerObject.getY(), 
                    playerObject.radius, 0, 2 * Math.PI);
            ctx.textAlign = 'center';
            ctx.fillText(playerObject.name, playerObject.getX(), playerObject.getY() - 15);
            ctx.fill();
            ctx.closePath();
        }
        setInterval(100)
    }

}
