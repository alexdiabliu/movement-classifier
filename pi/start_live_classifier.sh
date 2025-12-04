#!/bin/bash
cd /home/pi/final_project

# Activate virtualenv
source /home/pi/final_project/final_env/bin/activate

# Run the classifier (no blocking of boot, & to run in background)
python -u /home/pi/final_project/live_classifier.py >> /home/pi/final_project/live_classifier.log 2>&1 &
