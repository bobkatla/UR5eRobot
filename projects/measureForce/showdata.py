import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("robot_data.csv")

a = df["actual_TCP_force_2"]

a.plot()

plt.show()