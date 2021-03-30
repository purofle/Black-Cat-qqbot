import random

from graia.application import GraiaMiraiApplication
from graia.application.entry import GroupMessage
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import FullMatch
from graia.saya import Channel, Saya
from graia.saya.builtins.broadcast.schema import ListenerSchema

from .coolapk_token import request

__name__ = "coolapk"
__description__ = "获取酷安酷图"
__author__ = "purofle"
__usage__ = "在群内发送 酷图 即可"

saya = Saya.current()
channel = Channel.current()

channel.name(__name__)
channel.author(__author__)
channel.description(f"{__description__}\n使用方法：{__usage__}")


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[Kanata([FullMatch("酷安酷图")])],
    )
)
async def coolapk(app: GraiaMiraiApplication, group: Group, member: Member):
    await app.sendNudge(member, group)
    await app.sendGroupMessage(
        group, MessageChain.create([At(member.id), Plain(" 图片发送较慢，请稍等...")])
    )

    n = await request(
        "https://api.coolapk.com/v6/page/dataList?url=%2Ffeed%2FcoolPictureList%3FfragmentTemplate%3Dflex&title=&subTitle=&page=1"
    )

    choice_dict = random.choice(n)

    url = choice_dict["pic"]
    username = choice_dict["username"]
    tag = choice_dict["tags"]
    device = choice_dict["device_title"]

    msg = [
        At(member.id),
        Plain(" 用户名：{}\n使用设备：{}\n标签：{}".format(username, device, tag)),
        Image.fromNetworkAddress(url),
    ]
    await app.sendGroupMessage(group, MessageChain.create(msg))
