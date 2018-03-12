#!/bin/bash

for value in ../A3-examples/correct-test-programs/*.c
do
	echo $value
	./Parser $value
done
