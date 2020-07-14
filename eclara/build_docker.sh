

# docker rm clara_c
# docker build --rm=true -t clara_struct_match .


docker cp clara/clara/loop_structure.py clara_c:/usr/local/lib/python2.7/dist-packages/clara/loop_structure.py
docker cp clara/clara/fn_matching.py clara_c:/usr/local/lib/python2.7/dist-packages/clara/fn_matching.py
docker cp clara/clara/forcematching.py clara_c:/usr/local/lib/python2.7/dist-packages/clara/forcematching.py
docker cp clara/clara/repair.py clara_c:/usr/local/lib/python2.7/dist-packages/clara/repair.py
docker cp clara/clara/grader.py clara_c:/usr/local/lib/python2.7/dist-packages/clara/grader.py
# # docker cp clara/clara/feedback_python.py clara_c:/usr/local/lib/python2.7/dist-packages/clara/feedback_python.py
# # docker cp clara/clara/py_parser.py clara_c:/usr/local/lib/python2.7/dist-packages/clara/py_parser.py
# # docker cp clara/clara/c_parser.py clara_c:/usr/local/lib/python2.7/dist-packages/clara/c_parser.py


docker cp clara/clara/feedback.py clara_c:/usr/local/lib/python2.7/dist-packages/clara/feedback.py
# docker cp clara/clara/clustering.py clara_c:/usr/local/lib/python2.7/dist-packages/clara/clustering.py


docker cp clara/bin/clara clara_c:/usr/local/bin/clara










# docker run -ti -h --name clara_c clara clara_fmap clara match examples/c1.py examples/c2.py --entryfnc computeDeriv --args "[[[4.5]], [[1.0,3.0,5.5]]]" --ignoreio 1
# docker exec -it clara_c clara repair examples/c5.c examples/i5.c  --ins "[[1]]" --ignoreio 1 --verbose 0 --structrepair 1
# docker exec -it clara_c clara repair examples/c7.c examples/i7.c  --args "[[[4,2,1,3],4]]" --ignoreio 1 --verbose 1 --structrepair 1 --entryfnc sort_numbers_ascending



# docker exec -it clara_c clara repair demo/c7.c demo/i9.c  --args "[[[4,2,1,3],4]]" --ignoreio 1 --verbose 0 --structrepair 1 --entryfnc sort_numbers_ascending
# docker exec -it clara_c clara repair demo/c7.c demo/i7.c  --args "[[[4,2,1,3],4]]" --ignoreio 1 --verbose 0 --structrepair 1 --entryfnc sort_numbers_ascending
# docker exec -it clara_c clara feedback demo/c8.c demo/c9.c demo/i11.c  --ins "[[5]]" --ignoreio 1 --verbose 0 --structrepair 1 --entryfnc main
# docker exec -it clara_c clara repair demo/c9.c demo/i11.c  --ins "[[5]]" --ignoreio 1 --verbose 0 --structrepair 1 --entryfnc main

# docker exec -it clara_c clara feedback demo/c2.c demo/c2.c demo/i2.c --ins "[[1], [-1], [0]]" --dce 1
# docker exec -it clara_c clara feedback demo/c1.c demo/c1.c demo/i1.c --ins "[[3,1,2]]" --ipgen 0

# docker exec -it clara_c clara feedback demo/c3.c demo/c3.c demo/i3.c --ins "[[1,2]]" --fnmapping 1

# docker exec -it clara_c clara feedback demo/c7.c demo/c7.c demo/i7.c  --args "[[[4,2,1,3],4]]" --ignoreio 1 --verbose 0 --structrepair 1 --entryfnc sort_numbers_ascending



# docker exec -it clara_c clara grade demo/c5.c demo/i5.c --numc 1 --numi 1  --ins "[[1,2,3]]" --ignoreio 0 --verbose 0 --structrepair 0 --entryfnc main --ipgen 1

# docker exec -it clara_c clara grade demo/c4.c demo/c5.c demo/i4.c demo/i5.c --verbose 0 --numc 2 --numi 2 --ins "[[1,2,3], [2,3,1], [3,1,2]]"

docker exec -it clara_c clara grade demo/c7.c demo/i7.c demo/i8.c demo/i9.c  --numc 1 --numi 3 --args "[[[4,2,1,3],4]]" --ignoreio 1 --verbose 0 --structrepair 1 --entryfnc sort_numbers_ascending

