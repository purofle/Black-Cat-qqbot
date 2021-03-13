#!/usr/bin/env python3

import asyncio
from graia.broadcast import Broadcast
from graia.saya import Saya
from graia.saya.builtins.broadcast import BroadcastBehaviour

loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
saya = Saya(bcc)

saya.install_behaviours(BroadcastBehaviour(bcc))

import asyncio
from graia.application import Session, GraiaMiraiApplication
from graia.broadcast import Broadcast

loop = asyncio.get_event_loop()

app = GraiaMiraiApplication(
        broadcast=bcc,
        connect_info=Session(
            host="http://0.0.0.0:8080",
            authKey="12345678",
            account=3552600542,
            websocket=True)
        )

with saya.module_context():
    saya.require("functions.coolapk")
    saya.require("functions.translation")

try:
    app.launch_blocking()
except KeyboardInterrupt:
    exit()
