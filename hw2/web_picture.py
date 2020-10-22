from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
import time
import base64
import requests
from PIL import Image
import io

 
from datetime import timedelta
 

ALLOWED_EXTENSIONS = set(['png', 'PNG','jpg'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
app = Flask(__name__)

app.send_file_max_age_default = timedelta(seconds=1)
 
 
# @app.route('/upload', methods=['POST', 'GET'])
@app.route('/upload', methods=['POST', 'GET'])  
def upload():
    if request.method == 'POST':
        imgb = request.files['file']
 
        if not (imgb and allowed_file(imgb.filename)):
            return jsonify({"error": 1001, "msg": "check it is png、PNG"})
        
        print(request)      
        print("hi")  
         
        user_input = request.form.get("name")
        b64f = base64.b64encode(imgb.read())
        b64s = b64f.decode('utf-8')

        form = {'file':b64s}
        res = requests.post(url='https://ccs2.azurewebsites.net/api/ptrans', json={'file':b64s})


        img = res.content
        img_b64decode = base64.b64decode(img)
        img = io.BytesIO(img_b64decode)
        img = Image.open(img)
        img.save('./static/images/test.png')


        

        return render_template('upload_ok.html',userinput=user_input,val1=time.time())
 
    return render_template('upload.html')
 
 
if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=8987, debug=True)
