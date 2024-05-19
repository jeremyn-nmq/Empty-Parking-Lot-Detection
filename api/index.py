from flask import Flask, make_response, json
from flask_cors import CORS
import gzip
import sys
sys.path.append('../python')
from python import image_detect

app = Flask(__name__)
CORS(app)

@app.route('/api/getParkingMap', methods=['GET'])
def get_parking_map():
    parking_map = image_detect.detect_parking_spaces()
    content = gzip.compress(json.dumps(parking_map).encode('utf-8'), 5)
    response = make_response(content)
    response.headers['Content-length'] = len(content)
    response.headers['Content-Encoding'] = 'gzip'
    # print(parking_map)
    return response


if __name__ == '__main__':
    app.run(debug=True, port=3005)
