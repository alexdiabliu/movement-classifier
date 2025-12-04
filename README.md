# Movement Classifier (Raspberry Pi + Sense HAT)

Human-activity recognition pipeline that collects accelerometer data on a Raspberry Pi Sense HAT, trains a scikit-learn SVM, and runs a live classifier that paints the Sense HAT LED matrix with the predicted activity.

## Features
- Four activities: `0` sitting, `1` walking, `2` running, `3` turning clockwise (color-coded Blue/Red/Green/Yellow on the LED matrix).
- Data collection script driven by the Sense HAT joystick.
- Windowed feature extraction (mean/std/max/min of axes and magnitude) and linear SVM training.
- Pretrained model: `ml/svm_multiclass.joblib`.
- Live classifier for the Pi with start/pause/exit controls and a boot helper script.

## Project Layout
- `ml/svm_multiclass.joblib` - pretrained SVM model.
- `movement-classifier/ml/movement_classifier.ipynb` - end-to-end training notebook.
- `movement-classifier/training_data/` - raw accelerometer CSVs (`accel_0.csv` ... `accel_3.csv`) and `plot_tests.py` quick plots.
- `movement-classifier/pi/collect_data.py` - Sense HAT data logger with joystick controls.
- `movement-classifier/pi/live_classifier.py` - live HAR inference on the Pi.
- `movement-classifier/pi/start_live_classifier.sh` - example boot script to run the classifier headless.
- `movement-classifier/SVM HAR Paper.pdf` - reference paper.

## Requirements
- Raspberry Pi with Sense HAT (for data collection/inference).
- Python 3.9+ and pip.
- Python deps: `numpy`, `pandas`, `scikit-learn`, `matplotlib`, `joblib`, `sense-hat` (on the Pi).

## Collect Data on the Pi
Run from `movement-classifier/pi` with the Sense HAT attached:
```bash
python collect_data.py
```
Controls (joystick):
- `ENTER` cycles label (0 sitting / 1 walking / 2 running / 3 turningCW) and sets LED color.
- `UP` start recording, `DOWN` stop, `LEFT` exit.
Data saves to `accel_data.csv` with columns `timestamp,x,y,z,label`. Copy or rename into `movement-classifier/training_data/` as needed (e.g., `accel_4.csv`).

## Train and Evaluate
Open `movement-classifier/ml/movement_classifier.ipynb` and run all cells (requires the Python deps above). Pipeline details:
- Windows of `50` samples with stride `10`.
- Features: mean/std for x/y/z, mean/std/max/min for magnitude.
- Model: `StandardScaler` + linear `SVC (C=1.0, one-vs-rest)`.
- Last run results: `Model Accuracy: 94.32%` on a held-out test set (317 windowed samples); per-class precision/recall/f1 in the notebook output.
- The notebook saves `svm_multiclass.joblib` in the working directory; copy it to `ml/` (already included) and to the Pi runtime folder.

## Run the Live Classifier on the Pi
Place `live_classifier.py` and `svm_multiclass.joblib` together (e.g., `/home/pi/final_project`). Then:
```bash
python live_classifier.py
```
Controls:
- Middle button: toggle ON/OFF (paused shows white LEDs).
- Down button: exit.
Runtime parameters: window size `20`, inference every `0.05s`. LED colors: Blue=sitting, Red=walking, Green=running, Yellow=turningCW.

To run on boot, adjust paths in `pi/start_live_classifier.sh`, ensure your virtualenv is sourced, and enable it via your preferred startup method (e.g., systemd or rc.local).

## Quick Notes
- Training data labels must stay consistent with the live classifier color mapping.
- If you record new classes or change windowing, retrain via the notebook and redeploy the new `.joblib` to the Pi.
- For fast sanity checks, `training_data/plot_tests.py` plots raw axis traces for selected CSVs.
