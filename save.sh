#!/bin/bash
set -e

coral="192.168.100.2"

ssh mendel@$coral "screen -S coral -X at 0 stuff '^C'"
scp mendel@$coral:/home/mendel/out_video.avi /home/jcarnero
ssh mendel@$coral 'rm /home/mendel/out_video.avi'