import requests

from dotenv import load_dotenv

from homework import PRACTICUM_TOKEN

load_dotenv()

url = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
payload = {'from_date': 1549962000}
homework_statuses = requests.get(url, headers=headers, params=payload)
print(homework_statuses.text)
