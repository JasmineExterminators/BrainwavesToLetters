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

info = neurosity.get_info()
print(info)

def bitingALemon(data):
    print("data", data)
    # Switch light off/on
    
    # { probability: 0.93, label: "rightArm", timestamp: 1569961321174, metric: "kinesis" }

def leftArm(data):
    print("data", data)

unsubscribe = neurosity.kinesis("bitingALemon", bitingALemon)
unsubscribe = neurosity.kinesis("leftArm", leftArm)


# unsubscribe = neurosity.brainwaves_raw(callback)
time.sleep(15)
unsubscribe()
print("Done with example.py")