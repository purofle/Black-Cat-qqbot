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
    for i in data["avatars"]:
        _str += " {}星 {}级 {}: {}命\n".format(
            i["rarity"], i["level"], i["name"], i["actived_constellation_num"]
        )
    _word_str = "世界探索度：\n"
    for i in data["world_explorations"]:
        n = str(i["exploration_percentage"])
        n = n[-2:] + "." + n[2] + "%"
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
        n = format(avatars["data"])
        return n


print(
    asyncio.run(
        query(
            "_gid=GA1.2.1472705651.1628852548; _MHYUUID=ca00182a-9236-44af-852c-32e2a0f9404e; UM_distinctid=17b3f2db54f64-0ad9a8d275b94e-3d740e5b-100200-17b3f2db5516a; CNZZDATA1275023096=1467006308-1628850557-|1628850557; ltoken=ibcKI1sAhHlKurdOpXtl0IjCKM3RNyobFEzumwBQ; ltuid=275401245; cookie_token=CplAB3DncDTTiQgonr8zRhIdmg129vjRxZJCp5jY; account_id=275401245; _ga_KJ6J9V9VZQ=GS1.1.1628853892.1.0.1628853898.0; _ga=GA1.2.1827177516.1628852548; _gat=1",
            "501083500",
        )
    )
)
