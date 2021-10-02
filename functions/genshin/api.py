import asyncio
from aiohttp import request
import random
import string
import time
import uuid
import hashlib

def get_ds(query: str = None, body: dict = None): # Github-Womsxd/YuanShen_User_Info
    salt = "xV8v4Qu54lUKrEYFZkJhB8cuOh9Asafs"  # Github-@lulu666lulu
    n = salt
    i = str(int(time.time()))
    r = str(random.randint(100000, 200000))
    if body:
        b = json.dumps(body)
    else:
        b = ""
    if query:
        q = query
    else:
        q = ""
    c = md5("salt=" + n + "&t=" + i + "&r=" + r + "&b=" + b + "&q=" + q)
    return i + "," + r + "," + c


def get_headers(cookie: str):
    return {
        "Cookie": cookie,
        "User-Agent": "okhttp/4.8.0",
        "Referer": "https://app.mihoyo.com",
        "Accept-Encoding": "gzip, deflate, br",
        "x-rpc-channel": "miyousheluodi",
        "x-rpc-device_id": str(uuid.uuid3(uuid.NAMESPACE_URL, cookie))
        .replace("-", "")
        .upper(),
        "x-rpc-client_type": "2",
        "x-rpc-app_version": "2.8.0",
        "DS": get_ds(),
    }


def format(data: list) -> str:
    _str = "目前拥有：\n"
    for i in data["avatars"]:
        _str += " {}星 {}级 {}: {}命\n".format(
            i["rarity"], i["level"], i["name"], i["actived_constellation_num"]
        )
    _word_str = "世界探索度：\n"
    for i in data["world_explorations"]:
        n = str(i["exploration_percentage"]/10)+"%"
        _word_str += "{}探索度{}\n".format(i["name"], n)
    return _str + _word_str


async def query(cookie: str, uid: str):
    if uid[0] == "1":
        server = "cn_gf01"
    else:
        server = "cn_qd01"
    url = f"https://api-takumi.mihoyo.com/game_record/genshin/api/index?server={server}&role_id={uid}"
    async with request("GET", url, headers=get_headers(cookie)) as resp:
        avatars = await resp.json()
        try:
            n = format(avatars["data"])
        except TypeError:
            n = avatars
        return n
