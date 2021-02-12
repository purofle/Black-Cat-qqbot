from graia.application import GraiaMiraiApplication
from graia.application.group import Group, Member
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain
from apps import bcc
from graia.application.entry import GroupMessage
from functions.voice.api import AzureAPI
from functions.keys.key import read

read = read("config.yaml")["voice"]

@bcc.receiver(GroupMessage)
async def voice(
        app: GraiaMiraiApplication,
        group: Group,
        message: MessageChain,
        member: Member
        ):
    if message.asDisplay().startswith("语音列表"):
        azure = AzureAPI(read["location"], read["key"])
        text = await azure.get_voice_list()
        n = []
        for i in text[-23:]:
            n.append(i["LocalName"])
        await app.sendGroupMessage(group, MessageChain.create([Plain(str(n))]))
