import random
from hashlib import md5
from urllib.parse import urlencode
import aiohttp


class Fanyi:
    def __init__(
        self, q: str, to: str, appid: str, authKey: str, f: str = "auto"
    ) -> None:
        self.__q = q
        self.__form = f
        self.__to = to
        self.__appid = appid
        self.__autoKey = authKey
        self.__salt = random.randint(-10000, 100000)
        self.__sign: str = (
            str(self.__appid) + str(self.__q) + str(self.__salt) + self.__autoKey
        )
        __md5 = md5()
        __md5.update(self.__sign.encode(encoding="utf-8"))
        self.__sign = __md5.hexdigest()
        self.__values = urlencode(
            {
                "q": self.__q,
                "from": self.__form,
                "to": self.__to,
                "appid": self.__appid,
                "salt": self.__salt,
                "sign": self.__sign,
            }
        )
        self.__url = (
            "https://fanyi-api.baidu.com/api/trans/vip/translate?" + self.__values
        )

    async def get(self) -> str:
        async with aiohttp.request("GET", self.__url) as r:
            n = await r.json()
        try:
            print("!!!!n:", n)
            print("!!!!q:", self.__q)
            n = n["trans_result"][0]["dst"]
        except KeyError:
            return "出现错误！源数据：\n" + str(n)
        else:
            return n
