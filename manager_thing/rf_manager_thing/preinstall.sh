#!/bin/bash

git submodule init
git submodule update

git clone https://github.com/WiringPi/WiringPi.git
cd WiringPi
./build
gpio -v
cd -
rm -rf WiringPi

git clone https://github.com/nRF24/RF24.git
cd RF24
./configure
make
sudo make install
sudo apt-get install python3-dev libboost-python-dev -y
cd pyRF24
sudo ln -s $(ls /usr/lib/arm-linux-gnueabihf/libboost_python3*.so | tail -1) /usr/lib/arm-linux-gnueabihf/libboost_python3.so
python setup.py build
sudo python setup.py install
cd ../..
rm -rf RF24
