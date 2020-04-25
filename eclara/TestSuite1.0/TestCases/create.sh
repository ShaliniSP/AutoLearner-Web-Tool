a=28
while [ "$a" -lt 44 ]    # this is loop1
do
   # b="$a"

   echo $a

   cp p20_t.txt p${a}_t.txt
   a=`expr $a + 1`

done