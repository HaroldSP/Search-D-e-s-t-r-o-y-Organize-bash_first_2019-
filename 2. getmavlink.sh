#!/bin/bash

#sudo apt-get update 				#получение списка новых пактов
#sudo apt-get upgrade 				#непосредственное выполнение обновления пакетов

#sudo apt install git 				#установка Git 

#sudo apt install build-essential manpages-dev git automake autoconf 
						#компилятор GCC
#gcc --version 
						#проверка правильности установки и версия компилятора
#sudo apt-get install python3-pip 		#если нет Питона
#sudo apt install python-pip 			#если нет pip

#pip install future 				#устанавливаем Python future module
#sudo apt-get install python-dev libxml2 libxml2-dev libxslt-dev #устанавливаем заголовочные модули
#pip3 install lxml 				#устанавливаем lxml
#sudo pip2 install -U future lxml 		#устанавливаем lxml как сказано в README
#sudo apt install xmlto 			#устанавливаем дополнительную утилиту

#sudo apt-get install python-matplotlib 

#sudo apt-get install cmake 			#Если нет ни Makefile, ни configure, значит, программа использует 							#одну из альтернативных систем сборки: scons (присутствует файл 						#SConstruct) или cmake (CMakeLists.txt)
#sudo apt-get install checkinstall 		#если будем пользоваться утилитой checkinstall

#pip install pymavlink 				#устанавливаем pymavlink
#cd mavlink/pymavlink
#python setup.py install

cd || { echo "Failure, no such directory"; exit 1; } 
						#перехордим в домашний каталог, в противном случае сообщение об ошибке

git clone https://github.com/mavlink/mavlink.git --recursive 
						#скачиваем исходники

cd mavlink || { echo "Failure, no such directory"; exit 1; } 					
						#переходим в папку мавлинка
PYTHONPATH=$PWD

#rm "$PWD/CMakeCache.txt" 			#если первая установка прошла неудачно
mkdir build
cd build || { echo "Failure, no such directory"; exit 1; } 
cmake .. 					#обращаемся к каталогу на уровень выше

make
sudo make install

#sudo checkinstall				#продвинутый метод установки
#sudo dpkg -i "$PWD/test1.deb"

#python -m mavgenerate 				#генерирование библиотек с помощью графического интерфейса
#-m mod : run library module as a script (terminates option list)

#python -m pymavlink.tools.mavgen --lang=Python --wire-protocol=2.0 --output=/home/egor/mavlink/OUT1 message_definitions/v1.0/ardupilotmega.xml


