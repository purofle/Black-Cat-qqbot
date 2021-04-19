import aiohttp


class AzureAPI:
    def __init__(self, location: str, key: str) -> None:
        self.__location = location
        self.__key = key

    async def get_voice_list(self):
        async with aiohttp.request(
            "GET",
            "https://{}.tts.speech.microsoft.com/cognitiveservices/voices/list".format(
                self.__location
            ),
            headers={"Ocp-Apim-Subscription-Key": self.__key},
        ) as r:

            return await r.json()

    async def get_speech(self, text: str, speaker: str):
        """
        text: 要转换的文本
        speaker: 发音人
        """

        headers = {
            "Ocp-Apim-Subscription-Key": self.__key,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-48khz-96kbitrate-mono-mp3",
            "User-Agent": "curl",
        }

        data_raw = """<speak version='1.0' xml:lang='en-US'><voice xml:lang='en-US' xml:gender='Female' name='{}'>{}</voice></speak>""".format(
            speaker, text
        )

        url = "https://{}.tts.speech.microsoft.com/cognitiveservices/v1".format(
            self.__location
        )
        async with aiohttp.request("POST", url, data=data_raw, headers=headers) as r:
            n = await r.read()
            print(n)
            return n
