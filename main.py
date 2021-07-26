#!/usr/bin/env python3

import asyncio
import sys
from pathlib import Path

import yaml
from graia.application import GraiaMiraiApplication, Session
from graia.broadcast import Broadcast
from graia.saya import Saya
from graia.saya.builtins.broadcast import BroadcastBehaviour
from yaml.loader import SafeLoader

from utils.utils import get_all_package_name

loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
saya = Saya(bcc)

config_path = Path("config.yaml")
if not config_path.is_file():
    config_path.write_text(Path("config.yaml.sample").read_text())
    sys.exit(1)
config = yaml.load(config_path.read_text(), Loader=SafeLoader)

saya.install_behaviours(BroadcastBehaviour(bcc))
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host=config["mirai"]["host"],
        authKey=config["mirai"]["authKey"],
        account=config["mirai"]["account"],
        websocket=config["mirai"]["websocket"],
    ),
)

with saya.module_context():
    for i in get_all_package_name("functions/"):
        saya.require("functions.{}".format(i), config)

try:
    app.launch_blocking()
except KeyboardInterrupt:
    sys.exit()
