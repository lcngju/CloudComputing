
import pymongo
import flask
import bson.binary
from io import BytesIO
from PIL import Image

allow_formats = set(['jpeg', 'png', 'gif'])


app = flask.Flask(__name__)

app.debug = True
db = pymongo.MongoClient('localhost', 27017).test

def save_file(f):
    # print(f.read())
    content = BytesIO(f.read())
    try:
        img_type = Image.open(content).format.lower()
        if img_type not in allow_formats:
            raise IOError()
    except IOError:
        flask.abort(400)
        
    obj = dict(content= bson.binary.Binary(content.getvalue()), img_type = img_type)
    db.files.save(obj)
    
    return obj['_id']

@app.route('/f/<fid>')
def serve_file(fid):
    try:
        f = db.files.find_one(bson.objectid.ObjectId(fid))
        if f is None:
            raise bson.errors.InvalidId()
        return flask.Response(f['content'], mimetype='image/' + f['img_type'])
    
    except bson.errors.InvalidId:
        flask.abort(404)

@app.route('/upload', methods=['POST'])
def upload():

    f = flask.request.files['uploaded_file']
    fid = save_file(f)

    return flask.redirect('/f/'+str(fid))

@app.route('/')
def index():

    return '''
    <!doctype html>
    <html>
    <body>
    <form action='/upload' method='post' enctype='multipart/form-data'>
    <input type='file' name='uploaded_file'>
    <input type='submit' value='Upload'>
    </form>

    '''

if __name__ == '__main__':

    app.run(port=7777)
