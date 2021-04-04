from graia.application import GraiaMiraiApplication
from graia.application.entry import GroupMessage
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain
from graia.saya import Channel, Saya
from graia.saya.builtins.broadcast.schema import ListenerSchema
from .Ysck import Ysck
from .count import count

saya = Saya.current()
channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def tr(
    app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member
):
    if message.asDisplay().startswith("抽奖分析"):

        msg = message.asDisplay().split(" ")
        url = msg[1]

        ysck = Ysck(url)
        try:
            __n = []
            for i in [200, 100, 301, 302]:
                __n.append(count(await ysck.request(i)))
            n = __n
        except RuntimeError as e:
            n = "出现错误！\n{}".format(e)

        await app.sendGroupMessage(
            group, MessageChain.create([At(member.id), Plain(str(n))])
        )
