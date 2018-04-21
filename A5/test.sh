for f in *.c 
do
	echo $f 
	python3 Parser.py $f
	diff -wB "$f.ast" examples/"$f.ast"
	diff -wB "$f.cfg" examples/"$f.cfg"
	# diff -wB "$f.sym" examples/"$f.sym"
	diff -wB "$f.s" examples/"$f.s"
done