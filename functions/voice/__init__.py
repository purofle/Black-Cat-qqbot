import json

from graia.application import GraiaMiraiApplication
from graia.application.entry import GroupMessage
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Plain
from graia.saya import Saya
from graia.saya.builtins.broadcast.behaviour import ListenerSchema
from graia.saya.channel import Channel
from pathlib import Path
from graiax import silkcoder

from .api import AzureAPI
from .config import data

__sayamname__ = "voice"
__description__ = "合成语音"
__author__ = "purofle"
__usage__ = "在群内发送 语音 发音人 内容 即可,发音人可通过 语音列表 获取."

saya = Saya.current()
channel = Channel.current()

config = saya.current_env()["voice"]

channel.name(__sayamname__)
channel.author(__author__)
channel.description(f"{__description__}\n使用方法：{__usage__}")

azure = AzureAPI(config["location"], config["key"])


@channel.use(ListenerSchema([GroupMessage]))
async def speech_list(
    app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member
):
    if message.asDisplay().startswith("语音列表"):

        await app.sendGroupMessage(
            group,
            MessageChain.create(
                [At(member.id), Plain(" 发音人列表如下：{}".format(data))]
            ),
        )


@channel.use(ListenerSchema([GroupMessage]))
async def voice(
    app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member
):
    message_raw = message.asDisplay()
    if message_raw[:2] == "语音" and len(message_raw) > 4:
        sp_m = message_raw.split(" ")

        if not sp_m[1] in data.keys():
            await app.sendGroupMessage(
                group, MessageChain.create([At(member.id), Plain(" 发音人选择错误！")])
            )
            return

        if len(message.asDisplay()) > 200:
            await app.sendGroupMessage(
                group, MessageChain.create([At(member.id), Plain(" 字数过多！")])
            )
            return

        if len(sp_m) < 3:
            await app.sendGroupMessage(
                group,
                MessageChain.create(
                    [At(member.id), Plain(" 请按照格式发送！格式如下：\n语音 发音人 文本")]
                ),
            )
            return
        await app.sendGroupMessage(group, MessageChain.create([Plain("请稍后")]))
        text = "".join(sp_m[2:])
        # text为文本，sp_m[1]为发音人的名字
        informant = data[sp_m[1]]
        voice_raw = await azure.get_speech(text, informant)
        # 转码
        silk: bytes = await silkcoder.encode(voice_raw)
        voice_m = await app.uploadVoice(silk)
        await app.sendGroupMessage(group, MessageChain.create([voice_m]))


@channel.use(ListenerSchema([GroupMessage]))
async def updateList(
    app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member
):
    if message.asDisplay() == "更新列表" and member.id == 3272912942:
        print(await azure.get_voice_list())
        await app.sendGroupMessage(group, MessageChain.create([Plain("已发送至后台")]))
