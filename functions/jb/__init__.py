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
            name = "{}({})".format(member.name, member.id)
            if not jb.get(group.id):
                jb[group.id] = {}
            if not jb[group.id].get(name):
                jb[group.id][name] = 0
            jb[group.id][name] += 1
            await app.sendGroupMessage(
                group, MessageChain.create([At(member.id), Plain(" 你的jb-1")])
            )


# 砍别人的jb
@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def jbK(
    app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain
):
    if not message.has(At):
        return
    if message.get(Image)[0].imageId == "{7F7177D2-D24A-93F5-32BA-C50CCFD02F70}.jpg":
        at = message.get(At)[0]
        member_at = await app.getMember(group, at.target)
        name = "{}({})".format(member_at.name, at.target)
        if not jb.get(group.id):
            jb[group.id] = {}
        if not jb[group.id].get(name):
            jb[group.id][name] = 0
        jb[group.id][name] += 0.5
        await app.sendGroupMessage(
            group,
            MessageChain.create(
                [At(member.id), Plain(f" 砍了下{name}的jb, {name}的jb-0.5")]
            ),
        )


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def jb_top(
    app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain
):
    if jb.get(group.id):
        if message.asDisplay() == "jb排行榜":
            await app.sendGroupMessage(
                group,
                MessageChain.create([Plain("jb排行榜：\n{}".format(format(group, jb)))]),
            )
