import json

from graia.application import GraiaMiraiApplication
from graia.application.entry import GroupMessage
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Plain, Voice
from graia.saya import Saya
from graia.saya.builtins.broadcast.behaviour import ListenerSchema
from graia.saya.channel import Channel

from functions.keys.key import read
from functions.voice.api import AzureAPI

from graiax import silkcoder

read_c = read("config.yaml")["voice"]
saya = Saya.current()
channel = Channel.current()


@channel.use(ListenerSchema([GroupMessage]))
async def voice(
    app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member
):
    if message.asDisplay().startswith("语音列表"):

        with open("functions/res/speaker.json", "r") as f:
            n = json.loads(f.read())

        await app.sendGroupMessage(
            group,
            MessageChain.create(
                [At(member.id), Plain(" 发音人列表如下：{}".format(str(list(n.keys()))))]
            ),
        )


@channel.use(ListenerSchema([GroupMessage]))
async def voice(
    app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member
):
    message_raw = message.asDisplay()
    if message_raw[:2] == "草草":
        sp_m = message_raw.split(" ")
        with open("functions/res/speaker.json", "r") as f:
            n = json.loads(f.read())  # 加载数据

        if not sp_m[1] in n.keys():
            await app.sendGroupMessage(
                group, MessageChain.create([At(member.id), Plain(" 发音人选择错误！")])
            )
            return

        elif len(message.asDisplay()) > 50:
            await app.sendGroupMessage(
                group, MessageChain.create([At(member.id), Plain(" 字数过多！")])
            )
            return

        if len(sp_m) < 3:
            await app.sendGroupMessage(
                group,
                MessageChain.create(
                    [At(member.id), Plain(" 请按照格式发送！格式如下：\n草草 发音人 文本")]
                ),
            )
            return

        else:
            await app.sendGroupMessage(group, MessageChain.create([Plain("请稍后")]))
            text = message.asDisplay()[4 + len(sp_m[1]) :]
            # text为文本，sp_m[1]为发音人
            azure = AzureAPI(read_c["location"], read_c["key"])
            voice_raw = await azure.get_speech(text, n[sp_m[1]])
            # 转码
            open("voice.mp3", "wb").write(voice_raw)
            await silkcoder.encode("voice.mp3", "voice.silk")
            voice = await app.uploadVoice(open("voice.silk", "rb").read())
            await app.sendGroupMessage(group, MessageChain.create([voice]))
