#!/bin/bash
python3 -m esptool --chip esp32 --port $1 erase_flash;
python3 -m esptool --chip esp32 --port $1 --baud 460800 write_flash -z 0x1000 esp32-20220117-v1.18.bin;
export AMPY_PORT=$1
for i in `ls project`; do ~/.local/bin/ampy put project/$i; done