#!/bin/bash
# Install Linux build dependencies for dlib and OpenCV
apt-get update
apt-get install -y build-essential cmake libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev
