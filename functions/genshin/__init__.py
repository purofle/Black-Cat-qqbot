from .api import query
from graia.application import GraiaMiraiApplication
from graia.application.entry import GroupMessage
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Plain
from graia.saya import Saya
from graia.saya.builtins.broadcast.behaviour import ListenerSchema
from graia.saya.channel import Channel

saya = Saya.current()
channel = Channel.current()

config = saya.current_env()["genshin"]


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def genshin(
    app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member
):
    if message.asDisplay().startswith("!genshin "):
        uid = message.asDisplay().split(" ")[1]
        if len(uid) != 9:
            await app.sendGroupMessage(
                group, MessageChain.create([At(member.id), Plain(" Invalid uid!")])
            )
            return
        _s = await query(config["cookie"], uid)
        await app.sendGroupMessage(
            group, MessageChain.create([At(member.id), Plain(f" {_s}")])
        )
