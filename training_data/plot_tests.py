import os
print("Current working directory:", os.getcwd())

import pandas as pd
import matplotlib.pyplot as plt

# Load data
df0 = pd.read_csv("accel_0.csv")
df1 = pd.read_csv("accel_1.csv")

# First plot: Standing
plt.figure()
plt.plot(df0['timestamp'], df0['z'], color='blue')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (g)')
plt.title('Raw Accelerometer Data - Standing (z)')
plt.grid(True)

# Second plot: Walking
plt.figure()
plt.plot(df1['timestamp'], df1['z'], color='orange')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (g)')
plt.title('Raw Accelerometer Data - Walking (z)')
plt.grid(True)
plt.show()



# First plot: Standing
plt.figure()
plt.plot(df0['timestamp'], df0['y'], color='blue')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (g)')
plt.title('Raw Accelerometer Data - Standing (y)')
plt.grid(True)

# Second plot: Walking
plt.figure()
plt.plot(df1['timestamp'], df1['y'], color='orange')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (g)')
plt.title('Raw Accelerometer Data - Walking (y)')
plt.grid(True)
plt.show()



# First plot: Standing
plt.figure()
plt.plot(df0['timestamp'], df0['x'], color='blue')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (g)')
plt.title('Raw Accelerometer Data - Standing (x)')
plt.grid(True)

# Second plot: Walking
plt.figure()
plt.plot(df1['timestamp'], df1['x'], color='orange')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (g)')
plt.title('Raw Accelerometer Data - Walking (x)')
plt.grid(True)
plt.show()