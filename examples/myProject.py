# # from neurosity import NeurositySDK
# # from dotenv import load_dotenv
# # import os
# # import time

# # load_dotenv()

# # neurosity = NeurositySDK({
# #     "device_id": os.getenv("NEUROSITY_DEVICE_ID")
# # })

# # neurosity.login({
# #     "email": os.getenv("NEUROSITY_EMAIL"),
# #     "password": os.getenv("NEUROSITY_PASSWORD")
# # })

# # info = neurosity.get_info()
# # print(info)

# # def callback(data):
# #     print("data", data)
# #     # Switch light off/on
# #     # light.togglePower()

# #     # { probability: 0.93, label: "rightArm", timestamp: 1569961321174, metric: "kinesis" }


# # unsubscribe = neurosity.kinesis("rightArm", callback)

# # # unsubscribe = neurosity.brainwaves_raw(callback)
# # time.sleep(5)
# # unsubscribe()
# # print("Done with example.py")





# # ---------------------------------------------------------------------------------

# from neurosity import NeurositySDK
# from dotenv import load_dotenv
# import os
# import time

# load_dotenv()

# neurosity = NeurositySDK({
#     "device_id": os.getenv("NEUROSITY_DEVICE_ID")
# })

# neurosity.login({
#     "email": os.getenv("NEUROSITY_EMAIL"),
#     "password": os.getenv("NEUROSITY_PASSWORD")
# })

# info = neurosity.get_info()
# print(info)

# def callback(data):
#     print("data", data)
#     # Switch light off/on
#     # light.togglePower()

#     # { probability: 0.93, label: "rightArm", timestamp: 1569961321174, metric: "kinesis" }


# unsubscribe = neurosity.kinesis("rightArm", callback)

# # unsubscribe = neurosity.brainwaves_raw(callback)
# time.sleep(5)
# unsubscribe()
# print("Done with example.py")
