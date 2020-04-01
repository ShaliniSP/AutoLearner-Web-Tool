import os
import sys
import re
folder = os.path.join('sources',sys.argv[1])
c_file = re.compile(r".*\.c")

for f in os.listdir(folder):
    if(c_file.match(f)) is not None:
	    string = open(os.path.join(folder,f),"r").read()
	    print("Commenting #include from ",f)
	    string = string.replace("#include","//#include")
	    open(os.path.join(folder,f),"w").write(string)
