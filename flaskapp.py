from flask import *  
import os
import subprocess
import pdb
import re

app = Flask(__name__,  static_url_path = "",static_folder = "./submissions")  

@app.route('/start')  
def upload():  
    return render_template("index.html")  

@app.route('/makesubmission', methods = ["POST"])
def submit():

    os.mkdir(os.path.join(".", "sources", request.form.get("subid")))

    os.mkdir(os.path.join(".", "sources", request.form.get("subid")+"/correct"))
    os.mkdir(os.path.join(".", "sources", request.form.get("subid")+"/incorrect"))
    numc = 0
    numi = 0


    for file in request.files:
        actualfile = request.files[file]

        if actualfile.filename[actualfile.filename.find('.')+1:] not in ['c','py']:
            continue
        if file[-1] =='c':
            f_type = "correct"
            numc+=1

            if numc==1:
                cfile = file[file.rfind('/')+1:-1]
        else:
            f_type = "incorrect"
            numi+=1


            if numi==1:
                ifile = file[file.rfind('/')+1:-1]
        print(actualfile.filename)
        actualfile.save(os.path.join(".","sources", request.form.get("subid")+"/"+f_type, actualfile.filename.split(os.sep)[-1]))
    #./run.sh subid

    entryfnc = request.form.get("entryfnc")

    if entryfnc == '':
        entryfnc = 'main'

    # pdb.set_trace()


    print("clara_input", request.form.get("clara_input"))
    error1 = subprocess.call(["bash","makedir.sh", str(request.form.get("subid"))])

    error2 = subprocess.call(["bash","oldclara.sh", str(request.form.get("subid")), request.form.get("clara_input"),  request.form.get("input_type"), cfile, ifile, entryfnc])

    error3 = subprocess.call(["bash","newclara.sh", str(request.form.get("subid")), request.form.get("clara_input"), request.form.get("ipgen"), request.form.get("dce"), request.form.get("ranking"), request.form.get("fnmapping"), request.form.get("structrepair"), request.form.get("input_type"), str(numc), str(numi), entryfnc])
    if(error1!=0 and error2!=0 and error3!=0):
        abort(400)
    else:  
        return jsonify({}), 200

@app.route('/success', methods = ['GET'])  
def success():  
    return render_template("viewResults.html", name = request.args.get("subid"))  

@app.route('/getcode')
def getcode():
    print ("Here")
    fname = os.path.join(".", "sources", request.args.get("subid")) + "/incorrect/"+ request.args.get("fname")
    with open(fname, 'r') as f:
        text = f.read()

    return render_template("code.html", fname = request.args.get("fname"), content = text)
@app.route('/processop', methods = ['GET'])
def process():


    fname = os.path.join(".", "sources", request.args.get("subid")) + "/clara_"+ request.args.get("type")+".txt"
    with open(fname, 'r') as f:
        text = f.read()
    repairs = {}

    # l = [m.start() for m in re.finditer(text, /r"Repairing.*\n")]
    prevKey = None
    for r in re.finditer("Repairing.*\n", text):
        fname = text[r.span()[0]+len("Repairing") +1:r.span()[1]]
        fname = fname[fname.rfind('/')+1:fname.rfind('\n')]
        repairs[fname] = [r.span()[1]]
        if prevKey!=None:
            repairs[prevKey].append(r.span()[0])
        prevKey = fname


    r_pos = text.find("Ranking:")
    if prevKey:
        repairs[prevKey].append(r_pos)

    ranking = None
    if r_pos!=-1:
        ranking = text[r_pos+len("Ranking:"):]
        text = text[:r_pos]
        # Some processing here
        # ranking = ranking.split('\n')
        # r_dic = {}
        # for r in ranking:
        #     for f in r.split(' '):
        #         if f.find('sources')!=-1:
        #             fname = f[f.rfind('/')+1:]
        #     r_dic[fname] = r

    return render_template("clara_content.html", content = text, repairs = repairs,  ranking = ranking, subid = request.args.get("subid"))



@app.route('/ranking', methods = ['GET'])
def print_ranking():

    fname = os.path.join(".", "sources", request.args.get("subid")) + "/clara_new.txt"
    with open(fname, 'r') as f:
        text = f.read()

    mc_pos = text.find("Max Cost: ")
    nind = text[mc_pos+len("Max Cost: "):].find('\n')
    maxcost = text[mc_pos+len("Max Cost: "):mc_pos+nind+len("Max Cost: ")]

    r_pos = text.find("Ranking:")
    ranking_text = text[r_pos:]

    r_dic = {}

    # pdb.set_trace()
    for line in ranking_text.split('\n'):
        ind = line.find('Cost:  ')
        if ind == -1:
            continue
        ind2 = line[ind+len('Cost:  '):].find(' ')
        cost = float(line[ind+len('Cost:  '): ind+len('Cost:  ')+ind2])
        r_dic[line[:ind]] = cost

    return render_template("ranking.html", ranking = r_dic, maxcost = maxcost)


if __name__ == '__main__':  
    app.run(debug = True, port = 1000, host = "0.0.0.0")
