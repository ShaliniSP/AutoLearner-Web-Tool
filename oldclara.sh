#!/bin/sh


# 			$1		$2		  $3			$4 		$5		$6
#./runs.sh subid clara_input input_type		Cfile	ifile	entryfnc


input_type="--ins"
echo $3
if [ "$3" = "args" ]; then
	echo "Arg type is args"
	input_type="--args"
fi


docker exec -it clara_c clara repair sources/$1/correct/$4 sources/$1/incorrect/$5 $input_type "$2"  --entryfnc $6 > sources/$1/clara_old.txt
