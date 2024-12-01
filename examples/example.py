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
    app.isTongue = True

def onStep(app):
    global unsubscribe
    unsubscribe = neurosity.calm(callback)
    # if app.isTongue:
    #     unsubscribe = neurosity.calm(callback)
    # else:
    #     unsubscribe = neurosity.kinesis("leftArm", callback)

def onKeyPress(app, key):
    if key == 'j':
        app.isTongue = not app.isTongue

def callback(data):
    # Switch light off/on
    print(data)
    # predictions = data.get('predictions', None)
    # if predictions is not None:
    #     probability = predictions[0].get('probability', None)
    # else:
    #     print("No predictions!!!!!")
    # if probability is not None:
    #     print("Probability!!!Tongue:", probability)
    #     app.probability = probability
    # else:
    #     print("No probability data found in:", data)
    # { probability: 0.93, label: "rightArm", timestamp: 1569961321174, metric: "kinesis" }
    
# def leftArm(data):
#     # Switch light off/on
#     probability = data.get("confidence", None)
#     if probability is not None:
#         print("Probability!!!LeftArm:", probability)
#         app.probability = probability
#     else:
#         print("No probability data found in:", data)
#     # { probability: 0.93, label: "rightArm", timestamp: 1569961321174, metric: "kinesis" }

def redrawAll(app):
    if app.isTongue:
        drawLabel(f'probability:{app.probability}', 200,200)
    else:
        drawLabel(f'probabilityArm:{app.probability}', 200,200)

runApp()
# while True:
#     unsubscribe = neurosity.calm(callback)
    

# cmu_graphics.run() 


# unsubscribe = neurosity.brainwaves_raw(callback)
# time.sleep(500)
# unsubscribe()
# print("Done with example.py")

