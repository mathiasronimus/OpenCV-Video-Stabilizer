# OpenCV Video Stabilizer
## What does it do?
It takes a shaky video as input, and produces a less shaky video as output. So
far only mp4 files have been tested.
## How do I use it?
You'll first need to install python (3.6+), then numpy (https://pypi.org/project/numpy/),
then opencv (https://pypi.org/project/opencv-python/). Then, open a terminal in
the stabilization directory and run the program:
```
python stabilize.py <path to video to stabilize> <path to save video>
```
## How does it work?
It uses Phase Correlation (https://en.wikipedia.org/wiki/Phase_correlation). This
is resistant to noise and openCV makes it easy to use. It isn't ideal for all situations,
but this was originally written for stabilizing higher-noise IR images, which in theory
this approach is good for.
