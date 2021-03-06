#!/bin/bash 

if [[ $(id -u) > 0 ]]; then 
	echo "this tool needs root privileges"
        sudo $0
        exit
fi

apt-get update
if ! hash pip; then
	echo "python-pip is needed..."
	apt-get install -y python-pip
fi 
apt-get install -y python-dev 
apt-get install -y python-zmq
apt-get install -y libpgm-5.1-0
apt-get install -y libzmq3-dev || { 
	echo; 
	echo "ERROR: libzmq 4.x is needed!"
	echo; 
	echo "Install by yourself (from source) or install precompiled package"; 
	echo; 
	echo "Note: For RaspberryPi: "; 
	echo "     "; 
	echo "      https://github.com/ceremcem/libzmq-4.x-armhf-cca.git"; 
	echo; 
	echo "After installation, press enter to continue..."; read -p "Press Enter to continue";
	 }
pip install -U -r requirements.txt
