import requests
from requests import Response

from secret import API_KEY, FOLDER_ID

# Переменные для API
api_key = API_KEY
folder_id = FOLDER_ID

url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Api-Key {api_key}',
    'X-Folder-Id': folder_id
}


def get_response_from_yandex_gpt(message: str) -> Response:
    data = {
        "modelUri": f"gpt://{folder_id}/yandexgpt-lite/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "1000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Отвечай как можно более кратко"
            },
            {
                "role": "user",
                "text": message
            }
        ]
    }

    response = requests.post(url, json=data, headers=headers)

    return response
