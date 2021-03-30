import aiohttp


class MakeLink:
    def __init__(self, url: str) -> None:
        """
        __baseurl: 已经是api的url
        """
        # 原url替换为api的url并且加上必要的参数
        self.__baseurl = url.replace(
            "webstatic.mihoyo.com/hk4e/event/e20190909gacha/index.html",
            "hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog",
        )[:-5]

    async def getMaxSize(self):
        """
        获取最大Size.

        params:
            gacha_type: 池子类型
        """
        async with aiohttp.request("GET", self.__baseurl) as r:
            __r = await r.json()
        return __r["data"]["size"]

    async def request(self, gacha_type: int):
        __url = "{}&page=1&gacha_type={}".format(self.__baseurl, str(gacha_type))


# test
print(
    MakeLink(
        "https://webstatic.mihoyo.com/hk4e/event/e20190909gacha/index.html?authkey_ver=1&sign_type=2&auth_appid=webview_gacha&init_type=301&gacha_id=b8fd0d8a6c940c7a16a486367de5f6d2232f53&lang=zh-cn&device_type=mobile&ext=%7b%22loc%22%3a%7b%22x%22%3a-674.7301025390625%2c%22y%22%3a216.91856384277345%2c%22z%22%3a198.0345001220703%7d%2c%22platform%22%3a%22Android%22%7d&game_version=CNRELAndroid1.4.0_R2147343_S2348834_D2316848&region=cn_qd01&authkey=leZ3ryrIgCVpqXj7OET5A2DcoRJkxGsU403pl%2fG3AjxNwpiVC%2f2nEyyfw03d9A3d%2bnMRV8fzKv2hRxzf9faOIc2Bna3mStXL1CNpIVgc2VsAxVncapdvzxvcufBjwguiI8EVefG6EswnZNxjFJOcdaMHeaPZ0R4sR3u0nDsJUCuPFqpUWe7v0M2WsocH9R6h4iGDrEPQNce1XeCwuapElaVqULygq7skO5JwALUzjPjvVKPCNYh%2fjK8ARanftBB1RL4AhHq6f2%2f1MvS15xqNOmnAhW8lGlInf2p0cOzJ5z9%2b7zLPNXBbGY783HKYu%2brn9sl4s8C1EsyjFw4C55MhEAiNQzGxZHIlyWjtOFA6iqh%2fkPu2XRU8QGk9i4mhDEuUj8E2lEtXpwqunICkQde7lVF31H6D2LWPszpQjIVAPG7%2fDyqgMav4Vj714xH27oOTX8CHrH4d1svekkgZ3gFjxaPBVgTTJdtDzNiG2VzzhZ0zF2Qu86wIq%2fW7ArS1gP18grY9s4PAPk1pk%2fXzoyhSfKi5qgxHfHHnf0WnNtbkFfdcYwGY5X59aV8eP2Qo%2f6odfNYTGU04RKfQZbZ%2f2EFrzZ77JDDO7qjlA438dGEsNeKyRQKGqFPd34ahx%2fS7lVmMLt36D9KGKZW3HGohP7D6aQZ3YyLuSZrrO5mvoOdygm2ELzHl%2f0CKbC%2bsjXHdiLwzAzgDgoVn4qrQjtZx57lucLdEPmvv7xA1xkS5BbG%2bbSJLweg7qHoupfczEmrVRExfMkjgGBZ5ARMm1j9WNFIzZOeQ2wGyfmlLKViyHc%2bydX2Rve55aLpM2RYw1iaRq1JJXYeY1ujSxnywdN0YNz%2byG%2b52X8psIdHPXbbiH9U4PGy2%2b6p76tcpS0og6x8DmzRmNr08GgTQRFtdJo7AA%2bLP905nFRvYYqJn5jxTLlvBl16c3ZiBMU12ZfR0hIg2UR2iPMVpmIwbW9LhX79bVvLaEu1hKUKSVBLsfUg%2fktKubPGRuBUTLmobberexIZR39O7dUbXEoGBFD3y0gJ3Gj5X4d8zx23A7jwjnhHyM9MIOJLirDpwg19iRvyJ6tglAca3Qo7Rvz73HCfRWzuOJgKTkZ%2flG%2bLUQADFzK8OoLh2oYVHJUA6rwnRDpy6vUs4g9QiSCuRnnAnuMaXtK69pzuITngUqo43tpzXzSo4QxmH2WQRG1Xhpq4zwEwoKZYIADPLgmlekKaXi6pNIAYp7CCdtfazf7%2fb5znynJAuE6XJZNbrmOqxz8BP0xr69iP3Ms1zErddI14n3hxEzsnRo7u81s2AOSlH6U9sLJcQM2Fg9Q2eGMbNMG1niHdERTvDnZRdkGS4Wve3%2fGaGZEuuJob0uA%3d%3d&game_biz=hk4e_cn#/log"
    ).r()
)
