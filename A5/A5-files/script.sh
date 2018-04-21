for f in ../examples/*.c 
do 
	echo $f
	./test.sh $f
done