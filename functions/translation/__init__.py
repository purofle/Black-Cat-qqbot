from graia.application import GraiaMiraiApplication
from graia.application.entry import GroupMessage
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain
from graia.saya import Channel, Saya
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.saya.event import SayaModuleInstalled

from functions.keys.key import read
from functions.translation.fanyi import Fanyi

appid = read("config.yaml")["fanyi"]["appid"]
authKey = read("config.yaml")["fanyi"]["authKey"]


saya = Saya.current()
channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def tr(
    app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member
):

    msg = message.asDisplay()
    if msg.startswith("翻译"):
        if len(msg) == 2 or len(msg.split(" ")) <= 2:
            await app.sendGroupMessage(
                group,
                MessageChain.create(
                    [
                        # 不 加 参 数 是 坏 文 明
                        At(member.id),
                        Plain(' 找不到参数！\n请使用"翻译 文本 语言代码"使用此功能！\n语言代码参考：'),
                        Image.fromLocalFile("functions/res/fanyi.jpg"),
                    ]
                ),
            )
        else:
            msg_sp = msg.split(" ")
            fanyi = Fanyi(msg_sp[1], msg_sp[2], appid, authKey)
            lang_to = await fanyi.get()
            await app.sendGroupMessage(
                group, MessageChain.create([At(member.id), Plain(" " + lang_to)])
            )
