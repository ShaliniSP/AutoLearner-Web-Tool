from flask import *  
import os
import subprocess

app = Flask(__name__,  static_url_path = "",static_folder = "./submissions")  

@app.route('/start')  
def upload():  
    return render_template("index.html")  

@app.route('/makesubmission', methods = ["POST"])
def submit():
    #create a new submission folder here.
    #create a new folder with this things subid
    #put all the files inside it
    #run m.py on this submission thing
    #have some flag to see if the submissiosnare ready
    os.mkdir(os.path.join(".", "sources", request.form.get("subid")))
    for file in request.files:
        actualfile = request.files[file]
        print(actualfile.filename)
        actualfile.save(os.path.join(".","sources", request.form.get("subid"), actualfile.filename.split(os.sep)[-1]))
    #./run.sh subid
    error = subprocess.call(["bash","run.sh", str(request.form.get("subid")), request.form.get("moss"), request.form.get("jplag"), request.form.get("mossw"), request.form.get("jplagw")])
    if(error!=0):
        abort(400)
    else:  
        return jsonify({}), 200

@app.route('/success', methods = ['GET'])  
def success():  
    return render_template("viewResults.html", name = request.args.get("subid"))  

if __name__ == '__main__':  
    app.run(debug = True, port = 1000, host = "0.0.0.0")
