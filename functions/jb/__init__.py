from graia.application import GraiaMiraiApplication
from graia.application.entry import GroupMessage
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain
from graia.saya import Channel, Saya
from graia.saya.builtins.broadcast.schema import ListenerSchema
from .format import format

saya = Saya.current()
channel = Channel.current()

jb = {}


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def jba(
    app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain
):
    if message.has(Image):
        print(message.get(Image)[0].imageId)
        if (
            message.get(Image)[0].imageId
            == "{7F7177D2-D24A-93F5-32BA-C50CCFD02F70}.jpg"
        ):
            if not jb.get(group.id):
                jb[group.id] = {}
            if not jb[group.id].get(member.id):
                jb[group.id][member.id] = 0
            jb[group.id][member.id] += 1
            await app.sendGroupMessage(
                group, MessageChain.create([At(member.id), Plain(" 你的jb-1")])
            )


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def jbTop(
    app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain
):
    if jb.get(group.id):
        if message.asDisplay() == "jb排行榜":
            await app.sendGroupMessage(
                group,
                MessageChain.create([
                    Plain("jb排行榜：\n{}".format(format(group, jb)))
                    ])
                )
