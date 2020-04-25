**CL**uster **A**nd **R**ep**A**ir tool for introductory programming assignments

About
=====
This is an extension of the clustering and repair tool for introductory
programming assignments(CLARA), described in the following paper:
*Automated Clustering and Program Repair forIntroductory Programming Assignments*
(https://dl.acm.org/doi/10.1145/3192366.3192387 and https://arxiv.org/abs/1603.03165).


Requires
========
- C compiler
- Cython
  - `$ sudo aptitude install cython` (Debian)
  - `# dnf install Cython` (Fedora)
- lpsolve 5.5 (development files and library)
  - `$ sudo aptitude install lp-solve liblpsolve55-dev` (Debian)
  - `# dnf install lpsolve-devel` (Fedora)


Installation
============
- Run `make install` in this directory; or
- See docker installation below


Docker installation
===================
1) Build the image with: `docker build --rm=true -t clara .`
2) Run the container with: `docker run -ti -h clara --name clara clara /bin/bash`


Running
=======
- `make` from above installs a binary file called `clara`
- Run `clara help` or see examples below


Debian note
===========

On Debian system the following is required before running the tool: `export LD_LIBRARY_PATH=/usr/lib/lp_solve/`


Examples
========

The `examples/` directory contains some example programs:
- `c1.py` and `c2.py` are the correct examples from the paper
- `i1.py` and `i2.py` are the incorrect example from the paper
- `c3.py` is a constructed example.

NEW FEATURES!
-------------
The section below describes new features in CLARA

Grading
-------
To repair multiple incorrect programs use the 'grade' command. All correct and incorrect programs must be passed to CLARA, via the command line alog with the number of correct and number of incorrect solutions. 

Example:
clara grade TestSuite/p21_1_c.c TestSuite/p21_2_c.c TestSuite/p21_1_i.c TestSuite/p21_2_i.c --numc 2 --numi 2 --ins "[[1,2,3], [2,3,1], [3,1,2]]"  
This repairs multiple incorrect programs from multiple correct programs.


Dead Code Elimination
---------------------
If there is dead code present in a correct specification, the tool is now capable to eliminating it. This leads to the avoidance of unnecessary fixes to the incorrect program, which does not make any sense to the end user

Example:
clara repair p20_1_c.c p20_1_i.c --ins [[1], [-1], [0]] --dce 1

p20_1_c.c containes dead variables x,y,z



Input Generation
----------------
Lack of suffienct input leads to incorrect fixes. Using the --ipgen flag may help solve this issue

Example:
clara repair p21_1_c.c p21_1_i.c --ins [[3,1,2]] --ipgen 1 


Function Matching
-----------------
To repair an incorrect program with different functions names as the correct program
Set the fnmapping flag to 1



Structure Matching
------------------
To repair an incorrect program with different looping structure as the correct program
Set the structrepair flag to 1





Matching
--------

To test matching between `examples/c1.py` and `examples/c2.py` on inputs `[4.5]` and `[1.0,3.0,5.5]` use:
```
clara match examples/c1.py examples/c2.py --entryfnc computeDeriv --args "[[[4.5]], [[1.0,3.0,5.5]]]" --ignoreio 1
```

This should output `Match!`.

To test matching between `examples/c1.py` and `examples/c3.py` on inputs `[4.5]` and `[1.0,3.0,5.5]` use:
```
clara match examples/c1.py examples/c3.py --entryfnc computeDeriv --args "[[[4.5]], [[1.0,3.0,5.5]]]" --ignoreio 1
```

This should output `No match!`.

Repair (on two programs)
------------------------

To repair `examples/i1.py` using `examples/c1.py` on the same inputs as above, use:
```
clara repair examples/c1.py examples/i1.py --entryfnc computeDeriv --args "[[[4.5]], [[1.0,3.0,5.5]]]" --ingoreio 1
```

Clustering
----------

To cluster correct programs on the same inputs as above use:
```
mkdir clusters
clara cluster examples/c*.py --clusterdir clusters --entryfnc computeDeriv --args "[[[4.5]], [[1.0,3.0,5.5]]]" --ignoreio 1
```

This should produce two clusters in the directroy `clusters/` and two `.json` files with additional experssion extracted from the clusters.

Feedback
--------

To produce feedback from the above clusters for an incorrect program, for example `examples/i1.py`, use:
```
clara feedback clusters/c*.py examples/i1.py --entryfnc computeDeriv --args "[[[4.5]], [[1.0,3.0,5.5]]]" --ignoreio 1 --feedtype python
```

Note
----

You can add `--verbose 1` to any of the examples to obtain a more verbose output.
