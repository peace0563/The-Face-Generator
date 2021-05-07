from flask import Flask, request, jsonify, make_response
from PIL import Image 
import PIL
from flask_cors import CORS, cross_origin
from io import BytesIO
import base64
import pretrained_example  generate_random_image


app = Flask(__name__)
cors = CORS(app)


app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

def pil2datauri(data):
    img = generate_random_image(data)
    data = BytesIO()
    img.save(data, "JPEG")
    data64 = base64.b64encode(data.getvalue())

    return u'data:img/jpeg;base64,'+data64.decode('utf-8')


@app.route('/gen', methods=['OPTIONS', 'POST'])
def create_task():
    if request.method == "OPTIONS":
        return _build_cors_prelight_response()
    elif request.method == "POST":
        if not request.json:
            abort(400)
        data = request.json
        g = pil2datauri(data)
        return g, 201
    else:
        abort(400)

def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=False)