#!/bin/sh


#						$1		$2		$3		$4		$5
#./runs.sh subid moss jplag mossw jplagw

export PATH="/home/pradyumna/RELEASE/BIN_LINUX:$PATH"
#export PATH="/home/anushkini/Desktop/Coursework/Projects/PD/plagtool/RELEASE/BIN_LINUX:$PATH"
export PATH="/home/ubuntu/plagtool/RELEASE/BIN_LINUX:$PATH"


mkdir submissions/$1

if [ "$4" == "1" ]; then
	mkdir submissions/$1/mossw
	python3 mw.py $1
fi



if [ "$5" == "1" ]; then
	java -jar jplag-2.12.1-SNAPSHOT-jar-with-dependencies.jar -l c/c++ -r submissions/$1/jplagw/ -s sources/$1/
fi



if [ "$2" == "1" -o "$3" == "1" ]; then

python3 remove_include.py $1 #removes include statements in the C files

cd sources/$1/

#Convert to IR using Lance - generates ir.c files
for filename in ./*.c; do
	compile "$filename"
done

#Dead code elimination
for filename in ./*.ir.c; do
        dce "$filename"
done

#Symbol table cleanup
for filename in ./*.ir.c; do
        stcleanup "$filename"
done

cd ..
cd ..

fi



if [ "$2" == "1" ]; then

#Running MOSS
mkdir submissions/$1/moss/
python3 m.py $1

fi



if [ "$3" == "1" ]; then

mkdir sources/$1/jplagsub

mv sources/$1/*.ir.c sources/$1/jplagsub/

#Running JPlag
java -jar jplag-2.12.1-SNAPSHOT-jar-with-dependencies.jar -l c/c++ -r submissions/$1/jplag/ -s sources/$1/jplagsub/

fi
