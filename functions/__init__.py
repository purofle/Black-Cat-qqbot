from functions.keys.key import read

read = read("config.yaml")["functions"]

from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Plain
from apps import bcc
from graia.application.entry import GroupMessage

@bcc.receiver(GroupMessage)
async def gmsg(
        app: GraiaMiraiApplication,
        group: Group,
        member: Member,
        message: MessageChain
        ):

    if message.asDisplay() == "功能列表":
        await app.sendGroupMessage(
                group, MessageChain.create([
                    At(member.id),
                    Plain("""欢迎使用本QQBOT！
目前已经支持的功能有：
功能列表：查询都有哪些功能，
翻译：翻译文字，
coolapk：获得一张好看的壁纸""")
                    ]))

if read["translation"]:
    print("导入翻译模块")
    import functions.translation

if read["coolapk"]:
    print("导入酷安模块")
    import functions.coolapk
