import asyncio
from aiohttp import request
import random
import string
import time
import uuid
import hashlib


def random_string(len: int) -> str:
    return "".join(
        [random.choice(string.ascii_letters + string.digits) for n in range(len)]
    )


def hexdigest(text: str) -> str:
    md5 = hashlib.md5()
    md5.update(text.encode("utf-8"))
    return md5.hexdigest()


def get_DS() -> str:
    md5string = "dmq2p7ka6nsu0d3ev6nex4k1ndzrnfiy"
    i = int(time.time())
    r = random_string(6)
    c = hexdigest(f"salt={md5string}&t={i}&r={r}")
    return f"{i},{r},{c}"


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
        "DS": get_DS(),
    }


def format(data: list) -> str:
    _str = "目前拥有：\n"
    for i in data:
        _str += " {}星 {}级 {}: {}命\n".format(
            i["rarity"], i["level"], i["name"], i["actived_constellation_num"]
        )
    return _str


async def query(cookie: str, uid: str):
    if uid[0] == "1":
        server = "cn_gf01"
    else:
        server = "cn_qd01"
    url = f"https://api-takumi.mihoyo.com/game_record/genshin/api/index?server={server}&role_id={uid}"
    async with request("GET", url, headers=get_headers(cookie)) as resp:
        avatars = await resp.json()
        try:
            n = format(avatars["data"]["avatars"])
        except TypeError:
            n = avatars
        return n
