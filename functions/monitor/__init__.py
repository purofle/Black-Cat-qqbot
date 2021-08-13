import asyncio
from graia.application import GraiaMiraiApplication
from graia.application.entry import GroupMessage
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Plain
from graia.saya import Channel, Saya
from graia.saya.builtins.broadcast.schema import ListenerSchema

import mcstatus

saya = Saya.current()
channel = Channel.current()
config = saya.current_env()["monitor"]
server = mcstatus.MinecraftBedrockServer(config["ip"])


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def monitor(
    app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain
):
    if not group.id == config["group"]:
        return
    if message.asDisplay() == "开始监控":
        saya.broadcast.loop.create_task(monitor_loop(app, group))
        await app.sendGroupMessage(
            group, MessageChain.create([At(member.id), Plain(" 已开启")])
        )

    if message.asDisplay() == "在线人数":
        status = await server.async_status()
        await app.sendGroupMessage(
            group,
            MessageChain.create(
                [At(member.id), Plain(f" 目前在线人数：{status.players_online}")]
            ),
        )


async def monitor_loop(app: GraiaMiraiApplication, group: Group):
    while True:
        await asyncio.sleep(config["interval"])
        try:
            await server.async_status()
        except BaseException:
            await app.sendGroupMessage(
                group,
                MessageChain.create([At(config["managerId"]), Plain(" 服务器连接失败!")]),
            )
            return
