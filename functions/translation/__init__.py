from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain
from apps import app
from apps import bcc

from graia.application.entry import GroupMessage
from functions.translation.fanyi import Fanyi
from functions.keys.key import read

appid = read("config.yaml")["fanyi"]["appid"]
authKey = read("config.yaml")["fanyi"]["authKey"]

@bcc.receiver(GroupMessage)
async def tr(
        app: GraiaMiraiApplication,
        group: Group,
        message: MessageChain,
        member: Member):

    msg = message.asDisplay()
    if msg.startswith("翻译"):
        if len(msg) == 2 or len(msg.split(" ")) <= 2:
            await app.sendGroupMessage(group, MessageChain.create([
                # 不 加 参 数 是 坏 文 明
                At(member.id),
                Plain(" 找不到参数！\n请使用\"翻译 文本 语言代码\"使用此功能！\n语言代码参考："),
                Image.fromLocalFile("src/fanyi.jpg")
                ]))
        else:
            msg_sp = msg.split(" ")
            fanyi = Fanyi(msg_sp[1], msg_sp[2], appid, authKey)
            lang_to = await fanyi.get()
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id),
                Plain(" "+lang_to)
                ]))

print("翻译模块加载完成")
