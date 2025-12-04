import joblib
from sense_hat import SenseHat
import time
import numpy as np

model = joblib.load("svm_multiclass.joblib")

sense = SenseHat()

# --- Parameters ---
window_size = 20
sleep_dt = 0.05

# Rolling buffers
buf_x = []
buf_y = []
buf_z = []

program_on = False
last_press_time = 0.0


def show_ready_animation():
    g = (0, 80, 0)
    o = (0, 0, 0)

    check = [
        o,o,o,o,o,o,o,o,
        o,o,o,o,o,o,o,o,
        o,o,o,o,o,g,o,o,
        o,o,o,o,g,o,o,o,
        o,o,o,g,o,o,o,o,
        g,o,g,o,o,o,o,o,
        o,g,o,o,o,o,o,o,
        o,o,o,o,o,o,o,o,
    ]

    for _ in range(2):
        sense.clear(0, 0, 0)
        time.sleep(0.2)
        sense.clear(0, 80, 0)
        time.sleep(0.2)

    sense.set_pixels(check)
    time.sleep(1.0)

    sense.clear()


# Boot sequence
print("Starting Live HAR classifier...")
print("Middle button: start/stop classifier")
print("Down button: exit")

show_ready_animation()

# Paused screen = all white
sense.clear(255, 255, 255)
print("Classifier is PAUSED. Press middle button to start.")


try:
    while True:
        events = sense.stick.get_events()
        now = time.time()

        for e in events:
            if now - last_press_time < 0.25:
                continue
            last_press_time = now

            if e.action == "pressed":
                if e.direction == "middle":
                    program_on = not program_on
                    if program_on:
                        print("Classifier ON")
                        sense.clear()   # clear screen, ready for colours
                    else:
                        print("Classifier PAUSED")
                        sense.clear(255, 255, 255)  # paused = white

                elif e.direction == "down":
                    print("Exiting...")
                    sense.clear()
                    raise SystemExit

        # If paused, don't read or classify
        if not program_on:
            time.sleep(0.05)
            continue

        # --- Read accelerometer ---
        accel = sense.get_accelerometer_raw()
        x = accel["x"]
        y = accel["y"]
        z = accel["z"]

        buf_x.append(x)
        buf_y.append(y)
        buf_z.append(z)

        # Keep only last window_size samples
        if len(buf_x) > window_size:
            buf_x.pop(0)
            buf_y.pop(0)
            buf_z.pop(0)

        # Only predict when buffer is full
        if len(buf_x) == window_size:
            x_vals = np.array(buf_x)
            y_vals = np.array(buf_y)
            z_vals = np.array(buf_z)

            mag_vals = np.sqrt(x_vals**2 + y_vals**2 + z_vals**2)

            mean_x = x_vals.mean()
            mean_y = y_vals.mean()
            mean_z = z_vals.mean()

            std_x = x_vals.std()
            std_y = y_vals.std()
            std_z = z_vals.std()

            mean_mag = mag_vals.mean()
            std_mag = mag_vals.std()
            max_mag = mag_vals.max()
            min_mag = mag_vals.min()

            features = np.array([[
                mean_x, mean_y, mean_z,
                std_x, std_y, std_z,
                mean_mag, std_mag, max_mag, min_mag
            ]])

            pred = int(model.predict(features)[0])

            # Solid colour per class
            if pred == 0:         # sitting
                sense.clear(0, 0, 255)        # blue
            elif pred == 1:       # walking
                sense.clear(255, 0, 0)        # red
            elif pred == 2:       # running
                sense.clear(0, 255, 0)        # green
            elif pred == 3:       # turning CW
                sense.clear(255, 255, 0)      # yellow
            else:
                sense.clear(255, 255, 255)    # fallback = white

        time.sleep(sleep_dt)

except KeyboardInterrupt:
    sense.clear()
    print("\nStopped cleanly (KeyboardInterrupt).")
except SystemExit:
    sense.clear()
    print("Stopped cleanly (SystemExit).")
