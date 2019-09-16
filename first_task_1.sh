#!/bin/bash

function task {				# функция для обработки файлов в директории
for f in "$dir1"/*			# цикл для перебора файлов
do
	local file="${f##*/}"		# выделение имени файла из абсолютного пути
	if [[ -d "$f" ]]; then		# проверка - является ли файл директорией
		dir1=$f			# переход на уровень ниже
		task			# рекурсивный вызов функции для обработки файлов во вложенной директории
	else				
		local name="${file%.[^.]*}"			# выделение имени файла с помощью регулярного выражения
		local extension="${file:${#name} + 1}"		# выделение расширения файла
		local size=$(wc -c "$f" | awk '{print$1}')			# получение размера файла в байтах (выделение первого аргумента команды wc -c)
		local duration=$(ffprobe -i "$f" -show_entries format=duration -v quiet -of csv="p=0" -sexagesimal)	# получение длины видео с помощью библиотеки ffmpeg
		echo -e "$name \t $extension \t $size "B" \t $duration" >> result.xls		# составление строки вывода для файла .xls
		dir1=$dir		#возврат в первоначальную директорию
	fi
done
}

rm /Users/aleksejkozlov/result.xls		# удаление выходного файла, если такой существует
echo -n "Write a full path to the directory:"		# вывод в командную строку предложения о вводе нужной папки для перебора
read dir		# считывание данных из командной строки
dir1=$dir		# переменная для использования в функции
task		# вызов функции
