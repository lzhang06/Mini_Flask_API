from flask import Flask, jsonify, request, Response
import json
from Scrap_Marine import Scrap_Marine

app = Flask(__name__)

@app.route('/', methods=['GET'])
def read_data():
 # vessel ID/port/name
 # vesselID = request.args.get('vesselID')
    name = request.args.get('name')
    # port = request.args.get('port')
    vessels_info_json = Scrap_Marine(name)

    return jsonify(vessels_info_json)

test_value = 'QUEEN ELIZABETH'

if __name__ == '__main__':
	# port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run()

