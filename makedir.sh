#!/bin/sh


# 			$1	
#./runs.sh subid


mkdir submissions/$1

echo $1
docker exec -it clara_c mkdir sources/$1

docker exec -it clara_c mkdir sources/$1/correct
docker exec -it clara_c mkdir sources/$1/incorrect


for filename in ./sources/$1/correct 
do docker cp $filename clara_c:/home/clara/sources/$1/
# echo $filename
done
for filename in ./sources/$1/incorrect
do docker cp $filename clara_c:/home/clara/sources/$1/
# echo $filename
done
