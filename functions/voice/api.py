import aiohttp

class AzureAPI:
    def __init__(self, location: str, key: str) -> None:
        self.__location = location
        self.__key = key

    async def get_voice_list(self):
        async with aiohttp.request("GET", "https://{}.tts.speech.microsoft.com/cognitiveservices/voices/list".format(self.__location), headers={"Ocp-Apim-Subscription-Key": self.__key}) as r:

            return await r.json()
