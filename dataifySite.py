from flask import Flask, request, jsonify
import dataifySiteBackend as spotScript
import json
import pandas as pd
from flask_cors import CORS
import numpy as np

app=Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    print("request.files:", request.files)
    print("keys:", request.files.keys())
    print("request.form.get(year)", request.form.get('yearInQuestion'))
    print("request.form.get(numSongs)", request.form.get('numSongs'))
    if 'files' not in request.files:
        return jsonify({"error":"No file found"}), 400
    try:
        files = request.files.getlist('files')
        year = request.form.get('yearInQuestion')
        num = request.form.get('numSongs')

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    num = int(num)
    method = request.form.get('method')
    print(year)
    data = []
    for file in files:
        if not file.filename.endswith('.json'):
            return jsonify({"error": "Only .json files allowed"}), 400
        file_content = file.read().decode("utf-8")
        datai = json.loads(file_content)
        data.extend(datai)
    print("received data: ")
    result = spotScript.run(data, year, num, method)
    result = result.tolist()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)