#!/usr/bin/env python3

from graia.saya import Saya
from graia.broadcast import Broadcast
from graia.saya.builtins.broadcast import BroadcastBehaviour

import asyncio

loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
saya = Saya(bcc) # 这里可以置空, 但是会丢失 Lifecycle 特性

saya.install_behaviours(BroadcastBehaviour(bcc))
