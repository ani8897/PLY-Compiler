for f in *.c 
do
	echo $f 
	python3 Parser.py $f
	diff -B "$f.s" examples/"$f.s"
done