import mosspy
import sys
import os

userid = 355098774  #294425639 #

m = mosspy.Moss(userid, "python")

#m.addBaseFile("submission/a01.py")
#m.addBaseFile("submission/test_student.py")

# Submission Files
#m.addFile("submission/a01-sample.py")
m.addFilesByWildcard(os.path.join("./sources",sys.argv[1],"*.ir.c"))

url = m.send() # Submission Report URL

print ("Report Url: " + url)

# Save report file
m.saveWebPage(url, os.path.join("submissions",sys.argv[1],"moss","report.html"))

# Download whole report locally including code diff links
mosspy.download_report(url,os.path.join("submissions",sys.argv[1],"moss","report"), connections=8)
