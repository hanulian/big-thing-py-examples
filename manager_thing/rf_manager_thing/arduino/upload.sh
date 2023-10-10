#!/bin/bash

board_port=$1
app=$2
arduino-cli compile --fqbn arduino:samd:nano_33_iot $app -v
arduino-cli upload -p $board_port --fqbn arduino:samd:nano_33_iot $app
arduino-cli monitor -p $board_port
