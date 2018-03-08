#!/bin/bash

for value in *.c
do
	echo $value
	python3 assign3.py $value
done
