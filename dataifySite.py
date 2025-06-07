from flask import Flask, request, jsonify, render_template
import dataifySiteBackend as spotScript
import json
import pandas as pd
from flask_cors import CORS
import numpy as np
import ijson

app=Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 * 10  # 5 MB
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    print("checkpoint1")
    if 'files' not in request.files:
        return jsonify({"error":"No file found"}), 400
    try:
        files = request.files.getlist('files')
        year = request.form.get('yearInQuestion')
        num = int(request.form.get('numSongs'))
        method = request.form.get('method')
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    data = []
    for file in files:
        if not file.filename.endswith('.json'):
            return jsonify({"error": "Only .json files allowed"}), 400
        try:
            for item in ijson.items(file, 'item'):
                data.append(item)
        except Exception as e:
            return jsonify({"error": f"Failed to parse JSON: {str(e)}"}), 400
    result = spotScript.run(data, year, num, method)
    result = result.tolist()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)