from io import BytesIO
import random

from graia.application import GraiaMiraiApplication
from graia.application.entry import GroupMessage
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain
from graia.saya import Channel, Saya
from graia.saya.builtins.broadcast.schema import ListenerSchema
from pysstv import color, grayscale
from PIL import Image as img

__sayamname__ = "coolapk"
__description__ = "获取sstv"
__author__ = "purofle"
__usage__ = "在群内发送 sstv并带上图片 即可"

saya = Saya.current()
channel = Channel.current()

channel.name(__sayamname__)
channel.author(__author__)
channel.description(f"{__description__}\n使用方法：{__usage__}")


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
    )
)
async def coolapk(
    app: GraiaMiraiApplication, group: Group, member: Member, message: MessageChain
):
    if not message.asDisplay().startswith("sstv"):
        return
    if message.has(Image):
        await app.sendGroupMessage(
            group, MessageChain.create([At(member.id), Plain(" 转码较慢，请稍后...")])
            )
    else:
        await app.sendGroupMessage(
                group, MessageChain.create([At(member.id), Plain(" 消息内没有图片！！！")])
                )
        return
    image: Image = message.get(Image)[0]
    image = img.open(BytesIO(await image.http_to_bytes()))
    message.dict()
