#!/usr/bin/env python3

import asyncio

from graia.saya import Saya
from graia.saya.builtins.broadcast import BroadcastBehaviour

from graia.application import GraiaMiraiApplication, Session
from graia.broadcast import Broadcast
import sys

from utils.utils import get_all_package_name

loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
saya = Saya(bcc)

saya.install_behaviours(BroadcastBehaviour(bcc))

oop = asyncio.get_event_loop()

app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://0.0.0.0:8080",
        authKey="12345678",
        account=3552600542,
        websocket=True,
    )
)

with saya.module_context():
    for i in get_all_package_name("functions/"):
        saya.require("functions.{}".format(i))

try:
    app.launch_blocking()
except KeyboardInterrupt:
    sys.exit()
