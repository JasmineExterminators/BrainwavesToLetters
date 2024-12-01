from neurosity import NeurositySDK
from dotenv import load_dotenv
import os
import time


load_dotenv()

neurosity = NeurositySDK({
    "device_id": os.getenv("NEUROSITY_DEVICE_ID")
})

neurosity.login({
    "email": os.getenv("NEUROSITY_EMAIL"),
    "password": os.getenv("NEUROSITY_PASSWORD")
})

# info = neurosity.get_info()
# print(info)

def callback(data):
    # Switch light off/on
    print(data)
    # predictions = data.get('predictions', None)
    # probability = predictions[0].get('probability', None)
    # print(probability)
    # probability = data.get("confidence", None)
    # if probability is not None:
    #     print(data)
    #     print("Probability!!!Tongue:", probability)
    # else:
    #     print("No probability data found in:", data)
    # { probability: 0.93, label: "rightArm", timestamp: 1569961321174, metric: "kinesis" }

while True:
    unsubscribe = neurosity.calm(callback)