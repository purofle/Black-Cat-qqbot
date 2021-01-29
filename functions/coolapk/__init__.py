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

        n = await request("https://api.coolapk.com/v6/page/dataList?url=%2Ffeed%2FcoolPictureList%3FfragmentTemplate%3Dflex&title=&subTitle=&page=1&firstItem=24272618")

        choice_dict = random.choice(n)

        url = choice_dict["pic"]
        username = choice_dict["username"]
        tag = choice_dict["tags"]
        device = choice_dict["device_title"]

        msg = [
                At(member.id),
                Plain(""" 用户名：{}
使用设备：{}
标签：{}""".format(username, device, tag)),
                Image.fromNetworkAddress(url)
                ]

        await app.sendGroupMessage(group, MessageChain.create(msg))

print("酷安模块导入完成")
