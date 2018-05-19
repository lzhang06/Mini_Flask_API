from flask import Flask, jsonify, request, Response
import json
import os
from Scrap_Marine_BS4 import Scrap_Marine

import sys
import logging

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

@app.route('/query', methods=['GET'])
def read_data():
 # vessel ID/port/name
 # vesselID = request.args.get('vesselID')
 
    key_word = request.args.get('key_word')
    loc= request.args.get('location')

    search_type = request.args.get('search_type')

    # port = request.args.get('port')
    if ' ' in key_word:
    	key_word = key_word.replace(' ', '+')

  		
    vessels_info_json = Scrap_Marine(key_word, location = loc, search_type = search_type)

    return jsonify(vessels_info_json)



if __name__ == '__main__':
	# port = int(os.environ.get("PORT", 5000))
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0',  port=port, debug=True)


