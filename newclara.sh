#!/bin/sh


# 			$1		$2		  $3	$4	$5		$6			$7			$8			$9    $10 		$11
#./runs.sh subid clara_input ipgen dce ranking fnmapping structrepair	input_type, numc, numi, entryfnc


input_type="--ins"
echo $8
if [ "$8" = "args" ]; then
	echo "Arg type is args"
	input_type="--args"
fi



docker exec -it clara_c clara grade sources/$1/correct/* sources/$1/incorrect/* $input_type "$2" --ipgen $3 --dce $4 --fnmapping $6 --structrepair $7 --verbose 0 --numc $9 --numi ${10} --entryfnc ${11} > sources/$1/clara_new.txt


