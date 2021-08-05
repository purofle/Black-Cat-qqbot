from graia.application import GraiaMiraiApplication
from graia.application.event.messages import GroupMessage
from graia.application.group import Group, Member, MemberPerm
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Plain
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import FullMatch
from graia.saya import Channel, Saya
from graia.saya.builtins.broadcast.schema import ListenerSchema

import random

saya = Saya.current()
channel = Channel.current()

@channel.use(ListenerSchema(listening_events=[GroupMessage]),
inline_dispatchers=[Kanata([FullMatch("随机禁言")])])
async def jy(
    app: GraiaMiraiApplication,
    group: Group,
    member: Member):
    if group.accountPerm != MemberPerm.Administrator and member.permission == MemberPerm.Administrator:
        await app.sendGroupMessage(
            group,
            MessageChain.create([
                Plain("管理员？拿来把你")
            ]))
        return
    if not group.accountPerm == MemberPerm.Administrator:
        await app.sendGroupMessage(
            group,
            MessageChain.create([
                Plain("没管理禁nm")
            ]))
    else:
        randint = random.randint(1,60)
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),
            Plain(f" 恭喜{member.name}获得{randint}秒的禁言时间！")
        ]))
        await app.mute(group, member, randint)