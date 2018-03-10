#!/bin/bash

for value in *.c
do
	echo $value
	python3 grammar.py $value
done
