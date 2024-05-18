from flask import Flask, jsonify
import image_detect

app = Flask(__name__)

@app.route('/getParkingMap', methods=['GET'])
def get_parking_map():
    parking_map = image_detect.detect_parking_spaces()
    # print(parking_map)
    return jsonify(parking_map)

if __name__ == '__main__':
    app.run(debug=True)
