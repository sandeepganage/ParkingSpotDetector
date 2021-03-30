from flask import Flask
from util.util import DIR_DATA
import json
import time
import os

global config

app = Flask(__name__)


@app.route('/get_parking_results', methods=['POST'])
def process_cam_request():
    file = DIR_DATA + 'result.json'
    mtime = time.ctime(os.path.getmtime(file))
    print(mtime)
    with open(file) as f:
        data = json.load(f)

    return data


if __name__ == "__main__":
    app.run(debug=True, port=5000)