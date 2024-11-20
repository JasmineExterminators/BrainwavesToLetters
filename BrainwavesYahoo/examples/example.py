from neurosity import NeurositySDK
from dotenv import load_dotenv
import os
import time
from cmu_graphics import *


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

# class Prob:
#     def __init__(num):
#         self.num = num

def onAppStart(appInstance):
    global app
    app = appInstance
    app.probability = 50
    neurosity.kinesis("tongue", tongue)

# def onStep(app):
    

def tongue(data):
    # Switch light off/on
    probability = data.get("confidence", None)
    if probability is not None:
        print("Probability!!!:", probability)
        app.probability = probability
    else:
        print("No probability data found in:", data)
    # { probability: 0.93, label: "rightArm", timestamp: 1569961321174, metric: "kinesis" }
    

def redrawAll(app):
    drawLabel(f'probability:{app.probability}', 200,200)

# runApp()
while True:
    
    unsubscribe = neurosity.kinesis("tongue", tongue)
    
    # unsubscribe = neurosity.kinesis("leftArm", leftArm)

# cmu_graphics.run() 


# unsubscribe = neurosity.brainwaves_raw(callback)
time.sleep(500)
unsubscribe()
print("Done with example.py")

