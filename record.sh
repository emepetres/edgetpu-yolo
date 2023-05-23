#!/bin/bash
set -e

coral="192.168.100.2"

ssh mendel@$coral 'screen -S coral -d -m python3 edgetpu-yolo/record.py --device 3'
