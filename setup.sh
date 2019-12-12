#!/bin/bash

echo -e "\e[32m"
echo '
|======================|
|  Alarm Clock Server  |
|     by: Axiiom       |
|----------------------|
|   ___  _____  _____  | 
|  / _ \/  __ \/  ___| |
| / /_\ \ /  \/\ `--.  |
| |  _  | |     `--. \ | 
| | | | | \__/\/\__/ / |
| \_| |_/\____/\____/  |
|----------------------|
|     Initializing     |
|======================|
'                        

insudo=$(groups | grep sudo)
if [[ ${#insudo} -lt 1 ]]; then 
	echo -e "\e[32mCould not install dependencies because you are not a sudo user"
	echo "Attempting to continue with setup ...\n"
else
	echo -e "\e[32mInstalling dependencies ..."
	sudo apt-get update && sudo apt-get upgrade -y
	sudo apt-get install docker.io docker-compose -y
	echo -e "\e[32mDone\n"

	echo -e "\e[33mSetting up docker permission for $USER ..."
	sudo groupadd docker >> /dev/null
	sudo usermod -aG docker "$USER" >> /dev/null
	echo -e "\e[33mDone\n"

	echo -e "\e[33mStarting docker service ... "
	sudo systemctl start docker
	echo -e "\e[33mDone\n"
fi

echo -e "\e[32m\n"
echo '
 ______           _             
 |  _  \         | |            
 | | | |___   ___| | _____ _ _ 
 | | | / _ \ / __| |/ / _ \ __|
 | |/ / (_) | (__|   <  __/ |   
 |___/ \___/ \___|_|\_\___|_|
' 


echo -e "\e[34mSetting up docker network ... "
docker network create --driver=bridge --subnet=192.19.2.0/16 --gateway=192.19.2.1 dockernet
echo -e "\e[34mDone\n"

echo -e "Creating docker image from file ... "
docker build --tag axiiom/acs:2.0 .
echo -e "\e[34mDone\n"

echo -e "\e[34mSetting up docker instances ..."
docker-compose -f ${PWD}/docker/docker-compose.yml  up
echo -e "\e[34mDone\n"
