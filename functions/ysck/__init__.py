from graia.application import GraiaMiraiApplication
from graia.application.entry import GroupMessage
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain
from graia.saya import Channel, Saya
from graia.saya.builtins.broadcast.schema import ListenerSchema
from .Ysck import Ysck

saya = Saya.current()
channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def tr(
    app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member
):
    if message.asDisplay().startswith("抽奖分析"):

        msg = message.asDisplay().split(" ")
        rank = int(msg[-1])
        url = msg[1]

        ysck = Ysck(url)
        try:
            n = await ysck.request(rank)
        except RuntimeError as e:
            n = "出现错误！\n{}".format(e)
        await app.sendGroupMessage(
            group, MessageChain.create([At(member.id), Plain(str(n))])
        )
