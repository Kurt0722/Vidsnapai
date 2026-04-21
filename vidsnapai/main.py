from fileinput import filename
import os
import uuid
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'user_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    myid= uuid.uuid1()
    if request.method == "POST":
        print(request.files.keys())
        rec_id = request.form.get("uuid");
        desc =request.form.get("text");
        if not rec_id:
           rec_id = str(uuid.uuid4())
        input_files=[];
        for key,value in request.files.items():
            print(key,value);
            
            #upload file    
            file = request.files[key]
            if file:
                filename = secure_filename(file.filename)
                if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], rec_id)):
                    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], rec_id))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], rec_id, filename))
                # capture desc and save it in a file
                input_files.append(filename);
                with open(os.path.join(app.config['UPLOAD_FOLDER'], rec_id, "desc.txt"), "w") as f:
                    f.write(desc)
            for fl in input_files:
                file_path = os.path.join("user_uploads", rec_id, fl)

                with open(os.path.join("user_uploads", rec_id, "input_files.txt"), "a") as f:
                    f.write(f"file '{fl}'\n")
                    f.write("duration 4\n")
               
    return render_template("create.html",myid=myid)

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

if __name__ == "__main__":
    app.run(debug=True)