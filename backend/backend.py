from flask import Flask, session
from flask_restful import reqparse
from PIL import Image
from io import BytesIO
import base64
import backend_run_model as brm

app = Flask(__name__)

#key from Flask documentation, not secret
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

parser = reqparse.RequestParser()
parser.add_argument('upjson')
parser.add_argument('pngBase64')

image_model = brm.image_reader("model/letter_model.h5")

@app.route('/process', methods=['PUT'])
def textPost():
    args = parser.parse_args()
    imgUrl = args['pngBase64']

    rawUrl = imgUrl.replace("data:image/png;base64,", "")
    decodedPng = base64.b64decode(rawUrl)
    img = Image.open(BytesIO(decodedPng))
    file_name = "putwriting.png"
    img.save(file_name, "png")

    session["readText"] = image_model.read("putwriting.png")
    return 'ok', 201
    
@app.route('/process', methods=['GET'])
def textGet():
    return {
        "reading": session["readText"]
    }

if __name__ == '__main__':
    app.run()