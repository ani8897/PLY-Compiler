#!/bin/bash

for value in *.cfg
do
	echo $value
	diff $value A3-examples/correct-test-programs/$value -B
done
