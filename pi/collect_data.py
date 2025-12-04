from sense_hat import SenseHat
import csv, time

s = SenseHat()
s.set_imu_config(True, True, True)

# Label mapping
labels = {
    0: ("sitting", (0, 0, 255)),      # blue
    1: ("walking", (255, 0, 0)),      # red
    2: ("running", (0, 255, 0)),      # green
    3: ("turningCW", (255, 255, 0))   # yellow
}

current_label = 0
recording = False

filename = "accel_data.csv"
print("Controls:")
print("  ENTER = change label")
print("  UP = start recording")
print("  DOWN = stop recording")
print("  LEFT = exit")
print()
print("Starting in 3 seconds...")
time.sleep(3)

# Open CSV
with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "x", "y", "z", "label"])

    last_press_time = 0

    while True:
        events = s.stick.get_events()
        now = time.time()

        for e in events:
            if now - last_press_time < 0.25:
                continue
            last_press_time = now

            if e.action == "pressed":
                if e.direction == "middle":       # cycle label
                    current_label = (current_label + 1) % 4
                    name, col = labels[current_label]
                    s.clear(*col)
                    print(f"Label changed to {name} ({current_label})")

                elif e.direction == "up":         # start logging
                    recording = True
                    print("Recording started.")

                elif e.direction == "down":       # stop logging
                    recording = False
                    print("Recording stopped.")

                elif e.direction == "left":       # exit program
                    print("Exiting.")
                    s.clear()
                    exit()

        # Record data if active
        if recording:
            accel = s.get_accelerometer_raw()
            x, y, z = accel["x"], accel["y"], accel["z"]
            writer.writerow([time.time(), x, y, z, current_label])
            time.sleep(0.03)
