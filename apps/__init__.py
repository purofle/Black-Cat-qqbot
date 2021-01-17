import asyncio
from graia.application.entry import GraiaMiraiApplication
from graia.application.session import Session
from graia.broadcast import Broadcast

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
        broadcast=bcc,
        connect_info=Session(
            host="http://0.0.0.0:8080",
            authKey="12345678",
            account=3552600542,
            websocket=True
            )
        )
