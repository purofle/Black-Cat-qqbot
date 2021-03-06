#!/usr/bin/env python3

import asyncio
import sys

from graia.application import GraiaMiraiApplication, Session
from graia.broadcast import Broadcast
from graia.saya import Saya
from graia.saya.builtins.broadcast import BroadcastBehaviour

from utils.utils import get_all_package_name

loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
saya = Saya(bcc)

saya.install_behaviours(BroadcastBehaviour(bcc))

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
        saya.require(f"functions/{i}")
try:
    app.launch_blocking()
except KeyboardInterrupt:
    print("正在退出...")
    sys.exit()
