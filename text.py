"""import json


def extract_text_from_response(response):
    print("Ответ от YandexGPT:", response.text)
    data = json.loads(response.text)

    try:
        result = data.get('result', {})
        alternatives = result.get('alternatives', [])

        if alternatives:
            first_alternative = alternatives[0]
            message = first_alternative.get('message', {})
            text = message.get('text')

            if not text:
                raise KeyError

        else:
            raise KeyError

    except KeyError:
        text = "Я не хочу говорить на эту тему"

    return text"""
