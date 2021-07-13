import asyncio as aso
import pandas as pd
import subprocess
import socket

# async def count():
#     print("One")
#     await aso.sleep(0.0000000000001)
#     print("Two")

# async def main():
#     await aso.gather(count(), count(), count())

# if __name__ == "__main__":
#     import time
#     s = time.perf_counter()
#     aso.run(main())
#     elapsed = time.perf_counter() - s
#     print(f"{__file__} excecuted in {elapsed: 0.2f} seconds.")

# h = "10.10.10.7"
# subprocess.check_output(["python", "record.py", "--host", str(h), "--samples", "1", "--frequency", "5", "--config", "curQ_record_config.xml"])
# a = pd.read_csv("./robot_data.csv")
# actual_xyz = a.loc[0,:]

# print(actual_xyz)

HOST = "10.10.10.7"
PORT = 30002 # UR secondary client
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("connection done\n")

f = open ("storing.script", "rb")   #Robotiq Gripper
l = f.read(1024)
while (l):
    s.send(l)
    l = f.read(1024)

# subprocess.check_output(["python", "testSocketCommu.py"])

s.close()

# def moveTo(joints, a, v):
#     moving = "movej({0}, a={1}, v={2})\n".format(joints, a, v)
#     s.send(bytes(moving,'utf-8'))

# joints = [0.7, -0.8, 0.4, -1.9, -1.6, 1.23]
# # moving = "movej({0}, a=2.0, v=2.8)\n".format(joints)
# # s.send(bytes(moving,'utf-8'))
# moveTo(joints, 2.0, 1.8)