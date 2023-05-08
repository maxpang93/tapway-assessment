import requests
import string
import secrets
import base64
from random import randint
from datetime import datetime
import time

def generate_random_base64_string(N=50):
    random_chars = "".join(secrets.choice(string.ascii_letters) for _ in range(N))
    return base64.b64encode(bytes(random_chars,"utf-8")).decode("utf-8")

def generate_random_int_string(N=6):
    i_str = str(randint(1,10**N))
    while len(i_str) < N:
        i_str = "0" + i_str
    return i_str

NUMBER_OF_REQUESTS = 1000
NUMEBR_OF_PREDS_PER_REQUESTS = 3

def main():
    for i in range(NUMBER_OF_REQUESTS):
        data = {
            "device_id": generate_random_int_string(),
            "client_id": generate_random_int_string(),
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
            "data": {
                "license_id": generate_random_int_string(),
                "preds": [
                    {
                        "image_frame": generate_random_base64_string(randint(50,100)),
                        "prob": randint(0, 100) / 100,
                        "tags": ["high_quality"] if randint(0, 1) else ["low_quality"]
                    } for _ in range(NUMEBR_OF_PREDS_PER_REQUESTS)
                ]
            }
        }
        res = requests.post(url="http://0.0.0.0:5000", json=data)
        print(f"Request {i+1}: {res.text}")
        time.sleep(1)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"Finished in {(end - start)} s")

