import aiohttp


class Ysck:
    """ 原神抽卡信息查询工具. """

    def __init__(self, url: str) -> None:
        self.__baseurl = url.replace(
            "webstatic.mihoyo.com/hk4e/event/e20190909gacha/index.html",
            "hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog",
        )[:-5]

    async def getMaxSize(self) -> int:
        """

        Returns: (int):最大size.

        """
        # 查询最大size.
        async with aiohttp.request("GET", self.__baseurl) as r:
            __r = await r.json()
        if __r["retcode"] == -101:
            raise (RuntimeError(__r))
        return __r["data"]["size"]

    async def request(self, gacha_type: int) -> dict:
        """

        向api发送请求.

        Args: gacha_type(int): 常驻祈愿为200,新手祈愿为100,角色活动祈愿为301,武器活动祈愿为302.

        Returns: (dict):返回的json数据.

        """

        __url = "{}&page=1&gacha_type={}&end_id=0&size={}".format(
            self.__baseurl, str(gacha_type), await self.getMaxSize()
        )
        async with aiohttp.request("GET", __url) as r:
            n = await r.json()

        return n["data"]
