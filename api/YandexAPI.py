import aiohttp
from aiohttp import ClientSession


class YandexApi:
    def __init__(self, api_key: str, folder_id: str):
        self.api_key = api_key
        self.folder_id = folder_id
        self.url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Api-Key {self.api_key}',
            'X-Folder-Id': self.folder_id
        }

    async def get_response_from_yandex_gpt(self, message: str, session: ClientSession, dialog: list) -> dict:
        data = {
            "modelUri": f"gpt://{self.folder_id}/yandexgpt-lite/latest",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": "1000"
            },
            "messages": dialog + [
                {
                    "role": "user",
                    "text": message
                }
            ]
        }

        async with session.post(self.url, json=data, headers=self.headers) as response:
            return await response.json()