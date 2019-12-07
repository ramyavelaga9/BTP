from flask import Flask,render_template, jsonify, make_response,redirect,url_for
from flask import request,flash
import os,os.path
import json
app = Flask(__name__)
i=0

app.config['UPLOAD FOLDER']='static/img/'
app.config['SECRET_KEY'] = '12345'

@app.route('/')
def render_html():
  return render_template('draw.html')

@app.route('/', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file'] 
        # print(os.listdir(app.config['UPLOAD FOLDER'])) 
        length=len([name for name in os.listdir(app.config['UPLOAD FOLDER']) if os.path.isfile(app.config['UPLOAD FOLDER']+name)])
        # print(os.path.join(app.config['UPLOAD FOLDER'])+str(length)+'.png')
        _, file_extension = os.path.splitext(app.config['UPLOAD FOLDER']+f.filename)
        if f.filename == '':
            flash('No selected file')
            return redirect(request.url) 

        f.save(os.path.join(app.config['UPLOAD FOLDER'])+str(length)+file_extension)
        flash('File  '+f.filename+ ' successfully uploaded')
        # f.save(f.filename)  
        return render_template('draw.html')
        # return render_template("success.html", name = f.filename)  

@app.route('/add',methods=['POST'])
def get_value():
  global i
  image=request.form['image']
  filename, _ = os.path.splitext(image)
  print(i)
  image_dir=str(filename)+str(i)+'.json'
  with open(image_dir.replace('img','json'),'w') as f:
    json.dump(request.form.to_dict(flat=False),f)
  i+=1
  return jsonify(success=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
