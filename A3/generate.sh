#!/bin/bash

for value in *.c
do
	echo $value
	python3 Parser.py $value
done
