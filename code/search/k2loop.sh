#!/bin/zsh
cd ~/Scratch/k2-hunt
while [ ! -f STOP ]; do NUMBA_NUM_THREADS=1 .venv/bin/python scripts/k2drive.py $1 $2 >> res/drive_$1.log 2>&1; sleep 20; done
