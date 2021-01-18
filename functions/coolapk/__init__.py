from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import At, Image, Plain
from functions.coolapk.coolapk_token import request
import random
from apps import bcc
from graia.application.entry import GroupMessage

@bcc.receiver(GroupMessage)
async def coolapk(
        app: GraiaMiraiApplication,
        message: MessageChain,
        group: Group,
        member: Member
        ):
    if message.asDisplay() == "coolapk":

        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id),
            Plain(" 图片发送较慢，请稍等...")
            ]))

        n =  await request("https://api.coolapk.com/v6/page/dataList?url=%2Ffeed%2FcoolPictureList%3FfragmentTemplate%3Dflex&title=&subTitle=&page=1&firstItem=24272618")

        url = []
        msg = [At(member.id)]

        for i in n["data"]:
            url.append(i["pic"])

        for i in random.sample(url, 2):
            msg.append(Image.fromNetworkAddress(i))

        await app.sendGroupMessage(group, MessageChain.create(msg))
