# clear -x


# echo "Multiple repair - 2 correct and 2 incorrect programs"
# read -rsp $'Correct Program 1\n' -n1 key
# cat demo/c4.c
# read -rsp $'\n' -n1 key
# clear -x


# read -rsp $'Correct Program 2\n' -n1 key
# cat demo/c5.c
# read -rsp $'\n' -n1 key
# clear -x


# read -rsp $'Incorrect Program 1\n' -n1 key
# cat demo/i4.c
# read -rsp $'\n' -n1 key
# clear -x

# read -rsp $'Incorrect Program 2\n' -n1 key
# cat demo/i5.c
# read -rsp $'\n' -n1 key
# clear -x


# read -rsp $'Multi repair\n' -n1 key
# docker exec -it clara_c clara grade demo/c4.c demo/c5.c demo/i4.c demo/i5.c --verbose 0 --numc 2 --numi 2 --ins "[[1,2,3], [2,3,1], [3,1,2]]"
# read -rsp $'\n' -n1 key
# clear -x







# echo "Order of input - Greatest of 3 numbers example"

# read -rsp $'Correct Fix with input - [1,2,3]\n' -n1 key
# docker exec -it clara_c clara repair demo/c1.c demo/i1.c --ins "[[1,2,3]]" --ipgen 0
# read -rsp $'\n' -n1 key
# clear -x

# read -rsp $'Incorrect Fix with input - [3,1,2]\n' -n1 key
# docker exec -it clara_c clara repair demo/c1.c demo/i1.c --ins "[[3,1,2]]" --ipgen 0
# read -rsp $'\n' -n1 key
# clear -x

# read -rsp $'With ipgen flag and input - [3,1,2]\n' -n1 key
# docker exec -it clara_c clara repair demo/c1.c demo/i1.c --ins "[[3,1,2]]" --ipgen 1
# read -rsp $'\n' -n1 key
# clear -x







# echo "Dead Code Elimination - Positive or negative number"

# read -rsp $'Correct Program\n' -n1 key
# cat demo/c2.c
# read -rsp $'\n' -n1 key
# clear -x

# read -rsp $'Incorrect Program\n' -n1 key
# cat demo/i2.c
# read -rsp $'\n' -n1 key
# clear -x

# read -rsp $'Without DCE\n' -n1 key
# docker exec -it clara_c clara repair demo/c2.c demo/i2.c --ins "[[1], [-1], [0]]" --dce 0
# read -rsp $'\n' -n1 key
# clear -x

# read -rsp $'With DCE\n' -n1 key
# docker exec -it clara_c clara repair demo/c2.c demo/i2.c --ins "[[1], [-1], [0]]" --dce 1
# read -rsp $'\n' -n1 key
# clear -x



# echo "Function Mapping - Average of two numbers"

# read -rsp $'Correct Program\n' -n1 key
# cat demo/c3.c
# read -rsp $'\n' -n1 key
# clear -x


# read -rsp $'Inorrect Program\n' -n1 key
# cat demo/i3.c
# read -rsp $'\n' -n1 key
# clear -x

# read -rsp $'Original clara response\n' -n1 key
# docker exec -it clara_c clara repair demo/c3.c demo/i3.c --ins "[[1,2]]" --verbose 1
# read -rsp $'\n' -n1 key
# clear -x


# read -rsp $'With Fnmapping flag\n' -n1 key
# docker exec -it clara_c clara repair demo/c3.c demo/i3.c --ins "[[1,2]]" --fnmapping 1
# read -rsp $'\n' -n1 key
# clear -x









echo "Structural mismatch - Sorting example"
read -rsp $'Program to sort an array in ascending order\n' -n1 key
cat demo/c7.c
read -rsp $'\n' -n1 key
clear -x

read -rsp $'Incorrect program - 1 fewer loop\n' -n1 key
cat demo/i7.c
read -rsp $'\n' -n1 key
clear -x

read -rsp $'Original clara response\n' -n1 key
docker exec -it clara_c clara repair demo/c7.c demo/i7.c  --args "[[[4,2,1,3],4]]" --ignoreio 1 --verbose 1 --entryfnc sort_numbers_ascending --structrepair 0 
read -rsp $'\n' -n1 key
clear -x

read -rsp $'With struct match flag\n' -n1 key
docker exec -it clara_c clara repair demo/c7.c demo/i7.c  --args "[[[4,2,1,3],4]]" --ignoreio 1 --verbose 0 --structrepair 1 --entryfnc sort_numbers_ascending
read -rsp $'\n' -n1 key
clear -x


read -rsp $'Incorrect program - 1 extra loop\n' -n1 key
cat demo/i8.c
read -rsp $'\n' -n1 key
clear -x

read -rsp $'With struct match flag\n' -n1 key
docker exec -it clara_c clara repair demo/c7.c demo/i8.c  --args "[[[4,2,1,3],4]]" --ignoreio 1 --verbose 0 --structrepair 1 --entryfnc sort_numbers_ascending
read -rsp $'\n' -n1 key
clear -x


read -rsp $'Incorrect program - No code written\n' -n1 key
cat demo/i9.c
read -rsp $'\n' -n1 key
clear -x

read -rsp $'With struct match flag\n' -n1 key
docker exec -it clara_c clara repair demo/c7.c demo/i9.c  --args "[[[4,2,1,3],4]]" --ignoreio 1 --verbose 0 --structrepair 1 --entryfnc sort_numbers_ascending
read -rsp $'\n' -n1 key
clear -x


# read -rsp $'Incorrect program - Different function name and 1 less loop\n' -n1 key
# cat demo/i10.c
# read -rsp $'\n' -n1 key
# clear -x

# read -rsp $'With struct match and fnmapping flag\n' -n1 key
# docker exec -it clara_c clara repair demo/c7.c demo/i10.c  --ins "[[4,2,1,3,4]]" --ignoreio 1 --verbose 0 --structrepair 1 --fnmapping 1
# read -rsp $'\n' -n1 key
# clear -x

