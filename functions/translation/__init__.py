from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain
from apps import app
from apps import bcc

from graia.application.entry import GroupMessage

@bcc.receiver(GroupMessage)
async def tr(
        app: GraiaMiraiApplication,
        group: Group,
        message: MessageChain,
        member: Member):
    if message.asDisplay() == "test":
        await app.sendGroupMessage(group,
                MessageChain.create([
                    Plain("test!")
                    ]))

print("翻译模块加载完成")
